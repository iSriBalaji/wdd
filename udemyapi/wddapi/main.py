from fastapi import FastAPI
from database import engine
import models
from routers import auth, admin, device, users, facility, washer, dryer, device_config
from starlette import status
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
app.include_router(device_config.router)
app.include_router(admin.router)
app.include_router(users.router)
app.include_router(washer.router)
app.include_router(dryer.router)
app.include_router(facility.router)

models.Base.metadata.create_all(bind=engine) # we combine models.py and database.py here
# this only runs when the wdd.db does not exist

@app.get("/", status_code=status.HTTP_200_OK)
async def root():
    """
    return the home page [status of wdd]
    """
    return {"message": "Server Running: Detect Status of Washer and Dryer!\n Build by isribalaji - contact@isribalaji.in//"}