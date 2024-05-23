from fastapi import FastAPI
from database import engine
import models
from routers import auth, device
from fastapi.openapi.utils import get_openapi

app = FastAPI()

def get_custom_openapi():
    openapi_schema = get_openapi(
        title="WDD API",
        version="1.2.0",
        openapi_version="3.1.0",
        routes=app.routes,
    )
    return openapi_schema

app.openapi = get_custom_openapi


app.include_router(auth.router)
app.include_router(device.router)

models.Base.metadata.create_all(bind=engine) # we combine models.py and database.py here
# this only runs when the wdd.db does not exist
