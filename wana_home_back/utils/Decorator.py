from functools import wraps
from . import Schema, Returns, Recaptcha, Config
from django.http import QueryDict

require_version = int(Config.config.get('django', 'api-version', fallback='0'))


def version_check(func):
    if not require_version: return func

    def warpper(request, *args, **kwargs):
        try:
            request_version = int(request.COOKIES.get('api-version', '0'))
        except ValueError:
            return Returns.param_input_error('api version should be numeric')
        if request_version < require_version:
            return Returns.version_error(require_version)
        return func(request, *args, **kwargs)

    return warpper


def require_method(request_method_list):
    if type(request_method_list) != list:
        request_method_list = [request_method_list]

    def decorator(func):
        @wraps(func)
        def inner(request, *args, **kwargs):
            if request.method not in request_method_list:
                return Returns.request_method_error()
            return func(request, *args, **kwargs)

        return inner

    return decorator


captcha_session_key = Config.config.get('recaptcha', 'captcha_session_key', fallback='')


def require_captcha(func):
    if not captcha_session_key: return func

    @wraps(func)
    def inner(request, *args, **kwargs):
        if Recaptcha.prepare:
            if not request.session.get(captcha_session_key):
                return Returns.require_captcha('recaptcha', Recaptcha.public_key)
            request.session[captcha_session_key] -= 1
        return func(request, *args, **kwargs)

    return inner


def param_schema(method, schema: dict = None, any_key=None):
    if any_key is not None:
        _schema = Schema.Dict(any_key=any_key)
    else:
        _schema = Schema.Dict(schema)

    def decorator(func):
        @wraps(func)
        @require_method([method])
        def inner(request, *args, **kwargs):
            if method == 'GET':
                temp = request.GET.dict()
            elif method == 'POST':
                temp = request.POST.dict()
            else:
                raise Exception('Unknown method {}'.format(method))
            try:
                data = Schema.validate(temp, _schema, request=request)
            except Schema.ValidateException as e:
                return Returns.param_input_error(str(e))
            if method == 'GET':
                request.GET = QueryDict('', mutable=True)
                request.GET.update(data)
            elif method == 'POST':
                request.POST = QueryDict('', mutable=True)
                request.POST.update(data)
            return func(request, *args, **kwargs)

        return inner

    return decorator


def post_schema(schema=None, any_key=None):
    return param_schema('POST', schema, any_key)


def get_schema(schema=None, any_key=None):
    return param_schema('GET', schema, any_key)


require_POST = require_method(["POST"])
require_GET = require_method(["GET"])
