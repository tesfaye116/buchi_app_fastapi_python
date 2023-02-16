from fastapi import APIRouter, Body
from database.database import get_collection
from models.Customer import CustomerSchema
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse


router = APIRouter()


@router.post("", response_model=CustomerSchema)
async def create_customer(customer: CustomerSchema = Body(...)):
   # check if customer phone number already exists in the database
    if await get_collection("customers").find_one({"phone": customer.phone}):
        customer = await get_collection("customers").find_one({"phone": customer.phone})
        return JSONResponse(status_code=200, content={"status": "success", "message": "customer phone number already exists", "customerId": customer["_id"]})
    else:
        new_customer = jsonable_encoder(customer)
        await get_collection("customers").insert_one(new_customer)
        if new_customer:
            return JSONResponse(status_code=200, content={"status": "success", "customerId": new_customer["_id"]})
        else:
            return JSONResponse(status_code=400, content={"status": "error"})
