
# Buchi Pet Finder APP (Fast API)

My Pet Adopt application is a simple and easy to use web application that allows users to quickly search for adoptable pets in their local area. Using Fast API, the application quickly filters through pet adoptable listings and provides users with detailed information about each pet, including pictures, descriptions. With My Pet Adopt, you can quickly find the perfect pet for you and easily contact the pet's owner. My Pet Adopt helps to make pet adoption simple and easy.


## Author

- [@tesfaye girma](https://github.com/tesfaye116)


## Environment Variables

To run this project, you will need to add the following environment variables to your .env file

For mongodb :

`DATABASE_URL` = " "

`MONGO_INITDB_DATABASE` = " "

`MONGO_INITDB_ROOT_USERNAME` = " "

`MONGO_INITDB_ROOT_PASSWORD` = " "

For petfinder api :


`API_KEY` = " "

`SECRET` = " "


## Run Locally

Clone the project

```bash
  git clone https://github.com/tesfaye116/buchi_app_fastapi_python.git
```

Go to the project directory

```bash
  cd buchi_app_fastapi_python
```

docker compose

```bash
  docker compose up 
```

Start the server

```bash
  http://localhost:8000/docs
```

## Deployment on Render (https://render.com/) Here is the link to the deployed app on render :

https://buchi-app-fastapi.onrender.com/docs


## Run Tests (pytest) 

```bash
  python -m pytest -vv or python3 -m pytest -vv
```


## In pet finder api, If The Access Token Is Expired, The App Will Automatically Refresh The Token And Continue To Work. without any interruption. 




