import asyncio
import ethereum as APIEth
from fastapi import APIRouter, Body
from fastapi.encoders import jsonable_encoder


from database import (
    retrieve_students,
    retrieve_student,
)
from models import (
    WalletsSchema,
    ResponseModel,
    ErrorResponseModel,
)



router = APIRouter()


@router.get("/")
async def get_notes() -> dict:

    return {
        "message": "server is up and running!"
    }


@router.get("/balance/{address}")
async def get_token_balance(address: str) -> dict:
    """Get a token balance for a given address."""

    futures = [retrieve_student(address)]
    result = await asyncio.gather(*futures)
    return {"result": result}


@router.get("/top")
async def get_top_holders() -> dict:
    """Get top holders of a given token."""

    futures = [retrieve_students()]
    result = await asyncio.gather(*futures)
    if result:
        return {"top_holders": result}
    else:
        return {"error": "No holders found"}


@router.get("/weekly/{address}")
async def get_holder_weekly_change(address: str) -> dict:
    """Get weekly change of a given address."""

    futures = [APIEth.fetch_weekly_balance_change_by_address(address)]
    result = await asyncio.gather(*futures)
    print(result)
    return {"result": result}



