import pytest
from httpx import AsyncClient


# This code tests the endpoint for the main page of the API
# The client is passed as a parameter
# The client is used to make a GET request to the root endpoint
# The response is checked to make sure that the status code is 200
# The response is checked to make sure that the expected JSON is returned

@pytest.mark.anyio
async def test_read_main(client: AsyncClient):
    response = await client.get("/")
    assert response.status_code == 200

# This function is used to get the data from the database
@pytest.mark.anyio
async def test_get_pets(client: AsyncClient):
    response = await client.get("/api/v1/pets?limit=1")
    assert response.status_code == 200
    assert response.json()['status'] == "success"

# This code tests the get_pet API endpoint. It sends a GET request to the /api/v1/pets/63edd329692362f5488edbac endpoint,
# and checks that the response status code is 200 and the response JSON matches the expected result.


@pytest.mark.anyio
async def test_get_pet(client: AsyncClient):
    response = await client.get("/api/v1/pets/63edd329692362f5488edbac")
    assert response.status_code == 200
    assert response.json()['status'] == "success"


# Create a new pet by sending a multipart form data to the endpoint with the picture of the pet

@pytest.mark.anyio
async def test_create_pet(client: AsyncClient):
    # send multipart form data to the endpoint with the picture of the pet
    response = await client.post("/api/v1/pets", files={"file": open("static/download.jpeg", "rb")}, data={
        "type": "Rabbit",
        "gender": "male",
        "size": "small",
        "age": "adult",
        "goodWithChildren": True,
        # pjotos will be file name of the uploaded file
        "photos": "download.jpeg",
    })

# This test checks if the get_pet method returns 200 and the expected response when
# no pet is found.


@pytest.mark.anyio
async def test_get_pet_not_found(client: AsyncClient):
    response = await client.get("/api/v1/pets/63edd329692362f5488edba")
    assert response.status_code == 200
    assert response.json() == {
        "status": "success",
        "pet_detail": 'No pet found'
    }


# This test checks that the create customer endpoint returns a success response
# when a customer is successfully created.

@pytest.mark.anyio
async def test_create_customer(client: AsyncClient):
    response = await client.post("/api/v1/customers", json={
        "name": "Tesfaye",
        "phone": "1234567890"
    })
    assert response.status_code == 200
    assert response.json()['status'] == "success"


@pytest.mark.anyio
async def test_create_customer_already_exists(client: AsyncClient):
    response = await client.post("/api/v1/customers", json={
        "name": "Tesfaye",
        "phone": "1234567890"
    })
    assert response.status_code == 200
    assert response.json()['status'] == "success"
    assert response.json()['message'] == "customer phone number already exists"


# Test the POST method of the /api/v1/customers endpoint
# with no body. Should return a 422 error and a message
# describing the required fields.

@pytest.mark.anyio
async def test_create_customer_422(client: AsyncClient):
    response = await client.post("/api/v1/customers", json={})
    assert response.status_code == 422
    assert response.json() == {
        "detail": [
            {
                "loc": [
                    "body",
                    "name"
                ],
                "msg": "field required",
                "type": "value_error.missing"
            },
            {
                "loc": [
                    "body",
                    "phone"
                ],
                "msg": "field required",
                "type": "value_error.missing"
            }
        ]
    }


# This is a test for the POST /adoptions endpoint. It creates a new adoption request.
@pytest.mark.anyio
async def test_adoption_request(client: AsyncClient):
    response = await client.post("/api/v1/adoptions", json={
        "petId": "63edd329692362f5488edbac",
        "customerId": "63ee7727a705894972566f22"
    })
    assert response.status_code == 200
    assert response.json()['status'] == "success"


# Create a new adoption request with an invalid petId and customerId
# The petId and customerId are required fields, so the request should return status code 422
@pytest.mark.anyio
async def test_adoption_request_422(client: AsyncClient):
    response = await client.post("/api/v1/adoptions", json={})
    assert response.status_code == 422
    assert response.json() == {
        "detail": [
            {
                "loc": [
                    "body",
                    "petId"
                ],
                "msg": "field required",
                "type": "value_error.missing"
            },
            {
                "loc": [
                    "body",
                    "customerId"
                ],
                "msg": "field required",
                "type": "value_error.missing"
            }
        ]
    }
