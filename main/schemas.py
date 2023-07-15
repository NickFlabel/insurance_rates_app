from typing import List
from pydantic import BaseModel

class RateItem(BaseModel):
    cargo_type: str
    rate: str

class RatesModel(BaseModel):
    __root__: dict[str, List[RateItem]]

class PriceModel(BaseModel):
    price: float