from fastapi import APIRouter

# from sqlalchemy import text


router = APIRouter()


@router.get("/healthcheck")
async def healthcheck():
    return "Success!"
