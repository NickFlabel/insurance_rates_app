from tortoise import fields, models
from tortoise.contrib.pydantic import pydantic_model_creator


class CargoTypes(models.Model):

    name = fields.CharField(max_length=50, unique=True)


class Rates(models.Model):

    startdate = fields.DateField()
    rate = fields.FloatField()
    cargo_type_id = fields.ForeignKeyField('models.CargoTypes', related_name='rates')

    class Meta:
        unique_together = [('startdate', 'cargo_type_id')]

RatesPydantic = pydantic_model_creator(Rates, name='RatesModel')
CargoTypePydantic = pydantic_model_creator(CargoTypes, name='CargoTypeModel')
