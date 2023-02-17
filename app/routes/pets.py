import pathlib
from sched import scheduler
import shutil
import time
from typing import List, Any, Optional
from fastapi import File, Form, APIRouter, UploadFile
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from app.config.config import Settings
from app.database.database import get_collection

import requests

from app.models.Pet import PetSchema



router = APIRouter()

settings = Settings()


url = "https://api.petfinder.com/v2/animals"


access_token_list = []

# if access token is expired, get a new one from the petfinder api and save it to the .env file


def get_access_token():
    url_auth = "https://api.petfinder.com/v2/oauth2/token"

    payload = 'grant_type=client_credentials&client_id=' + \
        settings.API_KEY + '&client_secret=' + settings.SECRET
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    response = requests.request(
        "POST", url_auth, headers=headers, data=payload, verify=False)

    response = response.json()

    if response["access_token"]:
        access_token = response["access_token"]
        access_token_list.clear()
        access_token_list.append(access_token)
        return access_token_list
    else:
        return access_token_list


# get the access token from the petfinder api
get_access_token()


# create pet route with form data and file upload
@router.post("", response_model=PetSchema)
async def create_pet(
    type: str = Form(...),
    gender: str = Form(...),
    size: str = Form(...),
    age: str = Form(...),
    goodWithChildren: bool = Form(...),
    photos: List[UploadFile] = File(...),
):

    pet = PetSchema(
        type=type,
        gender=gender,
        size=size,
        age=age,
        goodWithChildren=goodWithChildren,
        photos=["http://localhost:8000/static/" +
                photo.filename for photo in photos],
    )

    new_pet = jsonable_encoder(pet)
    await get_collection("pets").insert_one(new_pet)

    # create a directory for the pet
    pathlib.Path(f"static").mkdir(parents=True, exist_ok=True)

    # save the files to the directory
    for photo in photos:
        with open(f"static/{photo.filename}", "wb") as buffer:
            shutil.copyfileobj(photo.file, buffer)

    if new_pet:
        return JSONResponse(status_code=200, content={"status": "success", "petId": new_pet["_id"]})
    else:
        return JSONResponse(status_code=400, content={"status": "error"})


@router.get("")
async def get_pets(type: Optional[str] = None, gender: Optional[str] = None, size: Optional[str] = None, age: Optional[str] = None, goodWithChildren: Optional[bool] = None, limit: int = 0):

    params = {
        "type": type if type else {"$exists": True},
        "gender": gender if gender else {"$exists": True},
        "size": size if size else {"$exists": True},
        "age": age if age else {"$exists": True},
        "goodWithChildren": goodWithChildren if goodWithChildren else {"$exists": True}
    },

    search_pets = await get_collection("pets").find({"$and": params}).limit(limit).to_list(length=limit)

    # search for pets including the petfinder api data and return the results to the user

    # search from petfinder api
    payload = {}
    headers = {
        'Authorization': 'Bearer ' + access_token_list[0]
    }

    # parameters for the api
    params = {
        'type': type,
        'gender': gender,
        'size': size,
        'age': age,
        'goodWithChildren': goodWithChildren,
        'limit': limit
    }

    response = requests.request(
        "GET", url, headers=headers, data=payload, params=params, verify=False)

    # convert the response to json
    response = response.json()

    try:
        response = response["animals"]
    except:
        response = response["title"]

    # create a list to store the pets
    pet_list_db = []
    pet_list_api = []

    # loop through the pets and add them to the list
    for pet in search_pets:
        pet_list_db.append(pet)

    for pet in response:
        if response:
            pet_list_api.append(response)
        else:
            pet_list_api.append(pet)

    # return the list of pets
    try:
        if search_pets:
            return JSONResponse(status_code=200, content={"status": "success", "pets_from_db": pet_list_db, "pets_from_petfinder_api": pet_list_api})
        elif limit == 0 and search_pets == []:
            return JSONResponse(status_code=200, content={"status": "success", "pets_from_db": 'Limit is required', "pets_from_petfinder_api": 'Limit is required'})
        else:
            return JSONResponse(status_code=200, content={"status": "success", "pets_from_db": 'No pets found', "pets_from_petfinder_api": 'No pets found'})
    except:
        print("error")
        return JSONResponse(status_code=400, content={"status": "error"})


@router.get("/{pet_id}")
async def get_pet(pet_id: str):
    pet_id = {"_id": pet_id}
    pet = await get_collection("pets").find_one(pet_id)

    if pet:
        return JSONResponse(status_code=200, content={"status": "success", "pet_detail": pet})
    elif pet == None:
        return JSONResponse(status_code=200, content={"status": "success", "pet_detail": 'No pet found'})
    else:
        return JSONResponse(status_code=400, content={"status": "error"})
