import asyncio
from tortoise.exceptions import IntegrityError
from datetime import datetime
from tortoise.transactions import atomic
import logging
from fastapi import HTTPException

from main.models.models import Rates, CargoTypes

logger = logging.getLogger()

class RatePoster:

    def __init__(self, data: dict) -> None:
        self.data = data

    @atomic()
    async def post(self):
        try:
            await asyncio.gather(*self._create_rate_tasks())
            return True
        except IntegrityError:
            return False
        
    def _create_rate_tasks(self):
        tasks = []
        for key in self.data.keys():
            for elem in self.data[key]:
                tasks.append(self._process_rate(key, elem))
        return tasks

    async def _process_rate(self, date: str, data: dict):
        cargo_type, _ =  await CargoTypes.get_or_create(name=data['cargo_type'])
        new_rate = await Rates.create(cargo_type_id=cargo_type, startdate=datetime.strptime(date, "%Y-%m-%d"), rate = data['rate'])
        return new_rate


class RateGetter:

    async def get(self):
        result = {}
        rates = await Rates.all()
        for rate in rates:
            result.setdefault(str(rate.startdate), [])
            cargo_type = await rate.cargo_type_id.first()
            result[str(rate.startdate)].append({'cargo_type': cargo_type.name, 'rate': str(rate.rate)})
        return result


class PriceGetter:

    def __init__(self, cargo_type: str, price: str, date: str) -> None:
        self.cargo_type = cargo_type
        self.price = price
        self.date = datetime.strptime(date, "%Y-%m-%d")

    async def get_price(self):
        cargo_type = await CargoTypes.get(name=self.cargo_type)
        if not cargo_type:
            raise HTTPException(status_code=404, detail='Cargo type not found')
        rate = await Rates.filter(cargo_type_id=cargo_type, startdate__lte=self.date).order_by('-startdate').first()
        if rate:
            shipment_price = int(self.price) * rate.rate
            return shipment_price
        else:
            raise HTTPException(status_code=404, detail='No applicable rate found for the given date')
