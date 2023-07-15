from fastapi import APIRouter
from main.schemas import PriceModel
from main.crud import PriceGetter

router = APIRouter(
    prefix='/api',
)

@router.get('/shipment', response_model=PriceModel)
async def get_price(price: str, date: str, cargo_type: str):
    price = await PriceGetter(price=price, date=date, cargo_type=cargo_type).get_price()
    return {'price': price}
