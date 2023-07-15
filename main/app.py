from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise
from main.routers import rates, shipments
import os
import dotenv

dotenv.load_dotenv()

app = FastAPI()

origins = ['*']

app.include_router(rates.router)
app.include_router(shipments.router)

register_tortoise(
    app,
    db_url=f'{os.getenv("DB_DRIVER")}://{os.getenv("DB_USER")}:' \
                          f'{os.getenv("DB_PASSWORD")}@{os.getenv("DB_HOST")}:' \
                          f'{os.getenv("DB_PORT")}/{os.getenv("DB_NAME")}',
    modules={"models": ["main.models.models"]},
    generate_schemas=True,
    add_exception_handlers=True,
)
