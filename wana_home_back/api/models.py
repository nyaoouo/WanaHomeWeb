from django.db import models


class HouseState(models.Model):
    server = models.IntegerField(db_index=True)
    territory_id = models.IntegerField(db_index=True)
    ward_id = models.IntegerField(db_index=True)
    house_id = models.IntegerField(db_index=True)
    price = models.IntegerField()
    owner = models.CharField(max_length=256)
    start_sell = models.IntegerField(db_index=True, default=0)

    class Meta:
        unique_together = (("server", "territory_id", "ward_id", "house_id"),)

    @property
    def size(self):
        if self.price < 4000000:
            return 1
        elif self.price <= 20000000:
            return 2
        else:
            return 3

    def get_data_dict(self):
        return {
            'price': self.price,
            'start_sell': self.start_sell,
            'size': self.size,
            'owner': self.owner,
        }

    def get_key_dict(self):
        return {
            'server': self.server,
            'territory_id': self.territory_id,
            'ward_id': self.ward_id,
            'house_id': self.house_id,
        }

    def get_dict(self):
        return self.get_key_dict() | self.get_data_dict()


class ChangeRecord(models.Model):
    house = models.ForeignKey(HouseState, on_delete=models.CASCADE)
    event_type = models.CharField(max_length=64)
    param1 = models.CharField(max_length=64, default='')
    param2 = models.CharField(max_length=64, default='')
    record_time = models.IntegerField()

    def get_dict(self):
        return {
            'house': self.house.get_key_dict(),
            'event_type': self.event_type,
            'param1': self.param1,
            'param2': self.param2,
            'record_time': self.record_time,
        }


class LastUpdate(models.Model):
    server = models.IntegerField(primary_key=True)
    last_update = models.IntegerField()

    def get_dict(self):
        return {'server': self.server, 'last_update': self.last_update, }


class ResponseCache(models.Model):
    server = models.IntegerField()
    type = models.IntegerField()
    data = models.BinaryField()

    class Meta:
        unique_together = (("server", "type"),)
