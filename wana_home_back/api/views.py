import time
import base64
from functools import lru_cache
from inspect import getfile, getsourcelines
from datetime import datetime, timedelta

from django.db import transaction
from django.http import HttpResponse
from django.conf import settings

from utils import Returns, Decorator, Schema as s, Recaptcha, Config
from . import models
from .Servers import get_server_token

one_day = timedelta(days=1)

try:
    from wh_crypt import validate_token
except ModuleNotFoundError:
    def validate_token(server_token, user_data):
        if not isinstance(user_data, str): return
        tkn_data = server_token.encode('utf-8')
        try:
            return bytes(b ^ tkn_data[i % len(tkn_data)]
                         for i, b in enumerate(base64.b64decode(user_data))).decode('utf-8', errors='ignore')
        except Exception:
            return


@lru_cache(maxsize=1024)
def get_house_price_check_time(timestamp):
    check_dt = datetime.fromtimestamp(timestamp)
    if check_dt.hour >= 2: check_dt += one_day
    return check_dt.replace(hour=2, minute=1, second=0).timestamp()


@Decorator.require_GET
@Decorator.require_captcha
def get_server_list(request):
    return Returns.success(data=[o.get_dict() for o in models.LastUpdate.objects.all()])


@Decorator.require_captcha
@Decorator.get_schema({'server': s.Int, 'territory_id': s.Int, 'ward_id': s.Int, 'house_id': s.Int})
def get_house_data(request):
    try:
        house = models.HouseState.objects.get(
            server=request.GET['server'],
            territory_id=request.GET['territory_id'],
            ward_id=request.GET['ward_id'],
            house_id=request.GET['house_id'],
        )
    except models.HouseState.DoesNotExist:
        return Returns.api_not_exists(request)
    changes = [row.get_dict() for row in models.ChangeRecord.objects.filter(house=house).order_by('-record_time')[:100]]
    return Returns.success(data=house.get_data_dict(), changes=changes)


@Decorator.require_captcha
@Decorator.get_schema({'server': s.Int, 'type': s.Int})
def get_server_state(request):
    server = request.GET['server']
    get_type = request.GET['type']
    try:
        update_data = models.LastUpdate.objects.get(server=server)
    except models.LastUpdate.DoesNotExist:
        return Returns.api_not_exists(request)
    try:
        cache_data = models.ResponseCache.objects.get(server=server, type=get_type)
    except models.ResponseCache.DoesNotExist:
        response = _get_server_state_response(server, get_type, update_data.last_update)
        models.ResponseCache.objects.get_or_create(server=server, type=get_type, defaults={'data': response.content})
        return response
    else:
        return HttpResponse(content=cache_data.data, content_type='application/json')


def run_time_test(func):
    if not settings.DEBUG: return func
    source = f"{func.__name__}({getfile(func)}:{getsourcelines(func)[1]})"

    def warpper(*args, **argv):
        start = time.perf_counter()
        rtn = func(*args, **argv)
        print(f"{time.perf_counter() - start:.2f}s in {source} with arg {args} , {argv}")
        return rtn

    return warpper


@run_time_test
def get_onsale(server: int):
    return [row.get_dict() for row in
            models.HouseState.objects.filter(server=server, start_sell__gt=0).order_by('-start_sell')]


@run_time_test
def get_changes(server: int, limit: int = 100):
    return [row.get_dict() for row in
            models.ChangeRecord.objects.filter(house__server=server).order_by('-record_time')[:limit]]


@run_time_test
def get_state(server: int, territory_id: int):
    return [row.get_data_dict() for row in models.HouseState.objects.filter(server=server, territory_id=territory_id).order_by('ward_id', 'house_id')]


def _get_server_state_response(server: int, get_type: int, last_update: int):
    if get_type < 0:
        return Returns.success(
            states={territory_id: get_state(server, territory_id) for territory_id in territories},
            onsale=get_onsale(server), changes=get_changes(server), last_update=last_update)
    elif get_type == 0:
        return Returns.success(onsale=get_onsale(server), changes=get_changes(server), last_update=last_update)
    else:
        return Returns.success(state=get_state(server, get_type), last_update=last_update)


territories = [
    339,  # 海雾村
    341,  # 高脚孤丘
    340,  # 薰衣草苗园
    641,  # 白银乡
    979,  # 雪景房
]
ward_cnt = 24
house_cnt = 60

full_price = {3000000, 3187500, 3375000, 3562500, 3750000,
              16000000, 17000000, 18000000, 19000000, 20000000,
              40000000, 42500000, 45000000, 47500000, 50000000, }

sync_data_schema = s.Dict(
    {str(territory_id): s.List(s.List(s.Tuple(s.Str, s.Int), length=house_cnt), length=ward_cnt)
     for territory_id in territories}
)


@run_time_test
@Decorator.version_check
@Decorator.post_schema({
    'server': s.Int,
    'data': s.Any,
})
@transaction.atomic
def sync_data(request):
    current_time = int(time.time())
    server = request.POST['server']
    new_data = request.POST['data']
    server_token = get_server_token(server)
    if server_token is None: return Returns.param_input_error("server is not in config")
    if server_token: new_data = validate_token(server_token, new_data)
    try:
        new_data = sync_data_schema.process(new_data, 'data')
    except s.ValidateException as e:
        return Returns.param_input_error(str(e))
    db_data = {}
    for row in models.HouseState.objects.select_for_update().filter(server=server).order_by('ward_id', 'house_id'):
        db_data.setdefault(row.territory_id, {}).setdefault(row.ward_id, {})[row.house_id] = row.owner, row.price
    new_house_state = []
    new_change_record = []
    for territory_id in territories:
        territory_data = new_data[str(territory_id)]
        for ward_id in range(ward_cnt):
            ward_data = territory_data[ward_id]
            for house_id in range(house_cnt):
                new_owner, new_price = ward_data[house_id]
                try:
                    old_owner, old_price = db_data[territory_id][ward_id][house_id]
                except KeyError:
                    new_house_state.append(
                        models.HouseState(
                            server=server, territory_id=territory_id, ward_id=ward_id, house_id=house_id,
                            price=new_price, owner=new_owner, start_sell=(0 if new_owner else current_time)
                        )
                    )
                    continue
                if old_owner != new_owner or not old_owner:
                    dbo = models.HouseState.objects.get(server=server, territory_id=territory_id, ward_id=ward_id, house_id=house_id)
                    if old_owner != new_owner:
                        if old_owner and new_owner:
                            new_change_record.append(models.ChangeRecord(house=dbo, event_type="change_owner",
                                                                         param1=old_owner, param2=new_owner, record_time=current_time))
                        else:
                            if old_owner:
                                new_change_record.append(models.ChangeRecord(house=dbo, event_type="start_selling",
                                                                             param1=old_owner, param2=str(new_price), record_time=current_time))
                                dbo.start_sell = current_time
                            else:
                                new_change_record.append(models.ChangeRecord(house=dbo, event_type="sold",
                                                                             param1=new_owner, param2=str(current_time - dbo.start_sell),
                                                                             record_time=current_time))
                                dbo.start_sell = 0
                    elif old_price > new_price:
                        new_change_record.append(
                            models.ChangeRecord(house=dbo, event_type="price_reduce", param1=str(old_price),
                                                param2=str(new_price), record_time=current_time, ))
                    elif old_price < new_price or new_price in full_price and get_house_price_check_time(dbo.start_sell) < current_time:
                        new_change_record.append(models.ChangeRecord(house=dbo, event_type="price_refresh",
                                                                     param1=f"{old_price}/{dbo.start_sell}/{get_house_price_check_time(dbo.start_sell)}",
                                                                     param2=f"{new_owner}/{new_price}/{current_time}",
                                                                     record_time=current_time))
                        dbo.start_sell = current_time
                    else:
                        continue

                    dbo.price = new_price
                    dbo.owner = new_owner
                    dbo.save()
    models.ResponseCache.objects.filter(server=server).delete()
    if new_house_state:
        models.HouseState.objects.bulk_create(new_house_state)
    if new_change_record:
        models.ChangeRecord.objects.bulk_create(new_change_record)
    models.LastUpdate.objects.update_or_create(server=server, defaults={'last_update': current_time})
    return Returns.success()


sync_ngld_schema = s.List(s.Tuple(s.Str, s.Int), length=house_cnt)


@run_time_test
@Decorator.version_check
@Decorator.post_schema({
    'server': s.Int,
    'territory_id': s.Int,
    'ward_id': s.Int,
    'data': s.Any,
})
@transaction.atomic
def sync_ngld(request):
    current_time = int(time.time())
    server = request.POST['server']
    territory_id = request.POST['territory_id']
    ward_id = request.POST['ward_id']
    new_data = request.POST['data']
    server_token = get_server_token(server)
    if server_token is None: return Returns.param_input_error("server is not in config")
    if server_token: new_data = validate_token(server_token, new_data)
    try:
        new_data = sync_ngld_schema.process(new_data, 'data')
    except s.ValidateException as e:
        return Returns.param_input_error(str(e))
    db_data = {}
    for row in models.HouseState.objects.select_for_update().filter(
            server=server,
            territory_id=territory_id,
            ward_id=ward_id
    ).order_by('house_id'): db_data[row.house_id] = row.owner, row.price

    new_house_state = []
    new_change_record = []

    for house_id, data in enumerate(new_data):
        new_owner, new_price = data
        try:
            old_owner, old_price = db_data[house_id]
        except KeyError:
            new_house_state.append(
                models.HouseState(
                    server=server, territory_id=territory_id, ward_id=ward_id, house_id=house_id,
                    price=new_price, owner=new_owner, start_sell=(0 if new_owner else current_time)
                )
            )
            continue
        if old_owner != new_owner or not old_owner:
            dbo = models.HouseState.objects.get(server=server, territory_id=territory_id, ward_id=ward_id, house_id=house_id)
            if old_owner != new_owner:
                if old_owner and new_owner:
                    new_change_record.append(models.ChangeRecord(house=dbo, event_type="change_owner",
                                                                 param1=old_owner, param2=new_owner, record_time=current_time))
                else:
                    if old_owner:
                        new_change_record.append(models.ChangeRecord(house=dbo, event_type="start_selling",
                                                                     param1=old_owner, param2=str(new_price), record_time=current_time))
                        dbo.start_sell = current_time
                    else:
                        new_change_record.append(models.ChangeRecord(house=dbo, event_type="sold",
                                                                     param1=new_owner, param2=str(current_time - dbo.start_sell),
                                                                     record_time=current_time))
                        dbo.start_sell = 0
            elif old_price > new_price:
                new_change_record.append(
                    models.ChangeRecord(house=dbo, event_type="price_reduce", param1=str(old_price),
                                        param2=str(new_price), record_time=current_time, ))
            elif old_price < new_price or new_price in full_price and get_house_price_check_time(dbo.start_sell) < current_time:
                new_change_record.append(models.ChangeRecord(house=dbo, event_type="price_refresh",
                                                             param1=f"{old_price}/{dbo.start_sell}/{get_house_price_check_time(dbo.start_sell)}",
                                                             param2=f"{new_price}/{current_time}",
                                                             record_time=current_time))
                dbo.start_sell = current_time
            else:
                continue

            dbo.price = new_price
            dbo.owner = new_owner
            dbo.save()

    models.ResponseCache.objects.filter(server=server).delete()
    if new_house_state: models.HouseState.objects.bulk_create(new_house_state)
    if new_change_record: models.ChangeRecord.objects.bulk_create(new_change_record)
    models.LastUpdate.objects.update_or_create(server=server, defaults={'last_update': current_time})
    return Returns.success()


captcha_session_key = Config.config.get('recaptcha', 'captcha_session_key', fallback='')
captcha_charge = int(Config.config.get('recaptcha', 'captcha_give', fallback='1'))


@Decorator.post_schema({'t': s.String()})
def captcha(request):
    if Recaptcha.prepare:
        if Recaptcha.validate(request.POST['t']):
            request.session[captcha_session_key] = captcha_charge
    return Returns.success()


def page_not_found(request, exception):
    return Returns.api_not_exists(request)
