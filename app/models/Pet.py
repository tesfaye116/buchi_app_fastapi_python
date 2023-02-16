import datetime
from pydantic import BaseModel, Field
from typing import Any, List, Optional
from bson import ObjectId


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


class PetSchema(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    type: str = Field(...)
    gender: str = Field(...)
    size: str = Field(...)
    age: str = Field(...)
    goodWithChildren: bool = True
    photos: List[Any] = []
    createdDate: datetime.datetime = datetime.datetime.now().strftime("%Y-%m-%d")

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "type": "dog",
                "gender": "gender",
                "size": "size",
                "age": "age",
                "goodWithChildren": True,
                "photos": ["http://localhost:8080/static/"]
            }
        }

