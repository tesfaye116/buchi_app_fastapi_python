import datetime
from bson import ObjectId
from typing import Optional, List, Any
from pydantic import BaseModel, Field, validator, ValidationError

class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid objectid")
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")


class AdoptSchema(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    petId: str = Field(...)
    customerId: str = Field(...)
    adoptedDate: datetime.datetime = datetime.datetime.now().strftime("%Y-%m-%d")
    createdDate: datetime.datetime = datetime.datetime.now().strftime("%Y-%m-%d")

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "petId": "5f9c8b1a1a0f0a2b2c2c2c2c",
                "customerId": "5f9c8b1a1a0f0a2b2c2c2c2c",
            }
        }


