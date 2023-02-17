import datetime
from typing import Any, Optional
from fastapi import APIRouter
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from app.database.database import get_collection


router = APIRouter()


# generate report for a given date range and return as json which is adoptedPetType and WeeklyAdoptionCount
@router.post("/")
async def generate_report(start_date: Optional[str] = None, end_date: Optional[str] = None):
    # data have two arrays, one for adoptedPetTypes and the other for weeklyAdoptionRequests
    data = {
        "adoptedPetTypes": [],
        "weeklyAdoptionRequests": []
    }
    # using adopts collection to get the data for the report generation
    adopts_collection = get_collection("adopts")
    # get all the data from the collection
    adopts = await adopts_collection.find().to_list(length=100)
    # count the number of each pet type that is adopted using petid as the key and the count as the value from pet collection
    pet_count = {}
    # get the pet collection
    def get_pet(petId): return get_collection("pets").find_one({"_id": petId})

    for adopt in adopts:
        # get the petid from the adopt collection
        petid = adopt["petId"]
        # check if the petid is in the pet_count dictionary
        if petid in pet_count:
            # if it is then increment the count
            pet_count[petid] += 1
        else:
            # if it is not then add it to the dictionary with the count of 1
            pet_count[petid] = 1

    for petid in pet_count:
        data_count = {
            "type": await get_pet(petid),
            "count": pet_count[petid]
        }
        # add the petid and count to the adoptedPetTypes array
        data["adoptedPetTypes"].append(data_count)
    # get the start date and end date from the request
    start_date = datetime.datetime.strptime(
        start_date, "%Y-%m-%d").strftime("%Y-%m-%d")
    end_date = datetime.datetime.strptime(
        end_date, "%Y-%m-%d").strftime("%Y-%m-%d")
    # convert the start date and end date to datetime
    start_date = datetime.datetime.strptime(start_date, "%Y-%m-%d")
    end_date = datetime.datetime.strptime(end_date, "%Y-%m-%d")
    # get the number of days between the start date and end date
    days = (end_date - start_date).days + 1

    # loop through the days
    for i in range(days):
        # add the date to the weeklyAdoptionRequests array
        data["weeklyAdoptionRequests"].append({
            "date": start_date + datetime.timedelta(days=i),
            "count": 0
        })
    # loop through the adopts collection
    for adopt in adopts:
        # get the date from the adopt collection
        date = adopt["adoptedDate"]
        # convert the date to datetime
        date = datetime.datetime.strptime(date, "%Y-%m-%d")
        # loop through the weeklyAdoptionRequests array
        for i in range(len(data["weeklyAdoptionRequests"])):
            # check if the date is in the weeklyAdoptionRequests array
            if date == data["weeklyAdoptionRequests"][i]["date"]:
                # if it is then increment the count
                data["weeklyAdoptionRequests"][i]["count"] += 1
    # return the data as json
    try:
        return JSONResponse(status_code=200, content={"data": jsonable_encoder(data)})
    except Exception as e:
        return JSONResponse(status_code=500, content={"message": str(e)})
