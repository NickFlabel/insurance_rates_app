from fastapi import APIRouter, HTTPException
from main.schemas import RatesModel
from main.crud import RatePoster, RateGetter
import asyncpg

router = APIRouter(
    prefix='/api',
)

@router.post('/rates', status_code=202)
async def create_rate(rates: RatesModel):
    rates_dict = rates.dict()['__root__']
    try:
        if not await RatePoster(data=rates_dict).post():
            raise HTTPException(status_code=409)
    except asyncpg.exceptions._base.InterfaceError:
        raise HTTPException(status_code=409)
    
@router.get('/rates')
async def get_rates():
    return await RateGetter().get()
