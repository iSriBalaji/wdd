from fastapi import APIRouter

router = APIRouter()
# auth requires separate port to run to authenticate users

@router.get("/auth")
async def auth():
    return {"token": "<PASSWORD>"}