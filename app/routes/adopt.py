from typing import Any, Optional
from fastapi import APIRouter
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from database.database import get_collection
import datetime

from models.Adopt import AdoptSchema


router = APIRouter()


# create adopt add route and check if the pet and customer exist
@router.post("", response_model=AdoptSchema)
async def create_adopt(adopt: AdoptSchema):
    # check if the pet exists and if the customer exists
    pet = await get_collection("pets").find_one({"_id": adopt.petId})
    customer = await get_collection("customers").find_one({"_id": adopt.customerId})

    if pet and customer:
        new_adopt = jsonable_encoder(adopt)
        await get_collection("adopts").insert_one(new_adopt)
        if new_adopt:
            return JSONResponse(status_code=200, content={"status": "success", "adoptionId": new_adopt["_id"]})
        else:
            return JSONResponse(status_code=400, content={"status": "error"})
    else:
        return JSONResponse(status_code=400, content={"status": "error", "message": "Pet or customer does not exist"})


@router.get("")
# get all adoptions with params of from and to date
async def get_adopts(from_date: Optional[str] = None, to_date: Optional[str] = None,limit: Optional[int] = 10):


    def get_pet(petId): return get_collection("pets").find_one({"_id": petId})

    def get_customer(customerId): return get_collection(
        "customers").find_one({"_id": customerId})

    if from_date and to_date:
        from_date = datetime.datetime.strptime(
            from_date, "%Y-%m-%d").strftime("%Y-%m-%d")
        to_date = datetime.datetime.strptime(
            to_date, "%Y-%m-%d").strftime("%Y-%m-%d")
        adoptions = await get_collection("adopts").find({"adoptedDate": {"$gte": from_date, "$lte": to_date}}).to_list(length=limit)
    else:
        adoptions = await get_collection("adopts").find().to_list(length=100)
    if adoptions:
        return JSONResponse(status_code=200, content={"status": "success", "adoptions":
                                                      [{"_id": adoption["_id"], "petId": adoption["petId"], "customerId": adoption["customerId"], "adoptedDate": adoption["adoptedDate"], "pet": await get_pet(adoption["petId"]), "customer": await get_customer(adoption["customerId"])} for adoption in adoptions]})
    elif adoptions == []:
        return JSONResponse(status_code=200, content={"status": "success", "adoptions": "No adoptions found between the given dates"})
    else:
        return JSONResponse(status_code=400, content={"status": "error"})
