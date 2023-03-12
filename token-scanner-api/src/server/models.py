from typing import Optional

from pydantic import BaseModel, EmailStr, Field


class WalletsSchema(BaseModel):
    wallet: float = Field(...)

    class Config:
        allow_population_by_field_name = True
        schema_extra = {
            "example": {
                "wallet": "balance"
            }
        }


def ResponseModel(data, message):
    return {
        "data": [data],
        "code": 200,
        "message": message,
    }


def ErrorResponseModel(error, code, message):
    return {"error": error, "code": code, "message": message}