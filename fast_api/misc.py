from fastapi import FastAPI
from fast_api import routes
from Secweb.XContentTypeOptions import XContentTypeOptions
from Secweb.StrictTransportSecurity import HSTS
from . import config

tags_metadata = [
    {
        "name": "Основные методы",
        # "description": "Основные методы",
    }
]

app = FastAPI(
    title="FastAPI",
    # description='Апі сервіс',
    version="0.0.1",
    contact={
        "name": "Anton",
        # "url": config.BASE_URL,
        "email": "lifquti@gmail.com",

    },
    openapi_tags=tags_metadata,
    # openapi_url="/openapi.json"
)

app.add_middleware(XContentTypeOptions)
app.add_middleware(HSTS, Option={'max-age': 31536000, 'preload': True})
app.include_router(routes.contract.formatted_router)
