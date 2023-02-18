from fastapi import FastAPI
from app.routes.pets import router as PetsRouter
from app.routes.customers import router as CustomersRouter
from app.routes.adopt import router as AdoptsRouter
from app.routes.report import router as ReportRouter

from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

from fastapi.staticfiles import StaticFiles


app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(PetsRouter, tags=["Pets"], prefix="/api/v1/pets")

app.include_router(CustomersRouter, tags=["Customers"], prefix="/api/v1/customers")

app.include_router(AdoptsRouter, tags=["Adopts"], prefix="/api/v1/adoptions")

app.include_router(ReportRouter, tags=["Report"], prefix="/api/v1/generateReport")


@app.get("/", tags=["Root"])
async def read_root():
    my_cv = {
            "message": "Welcome to my Buchi's Pet App Made with Love by Tesfaye Girma ... to see the API documentation, go to /docs",
            "name": "Tesfaye Girma",
            "email": "tesfayegirma360@gmail.com",
            "phone": "+251 90 410 2123",
            "Job": "Full Stack Developer",
            "skills": [
                {"name": "Python", "level": "Advanced"},
                {"name": "JavaScript", "level": "Advanced"},
                {"name": "TypeScript", "level": "Advanced"},
                {"name": "React", "level": "Advanced"},
                {"name": "Django", "level": "Advanced"},
                {"name": "MongoDB", "level": "Advanced"},
                {"name": "PostgreSQL", "level": "Advanced"},
                {"name": "MySQL", "level": "Intermediate"},
                {"name": "Docker", "level": "Intermediate"},
                {"name": "Git", "level": "Advanced"},
                {"name": "Linux", "level": "Intermediate"},
            ],
            "languages": [
                {"name": "English", "level": "Advanced"},
                {"name": "Amharic", "level": "Native"}
            ],
            "interests": [
                "Python",
                "JavaScript",
                "TypeScript"
            ]
        }


        #make it json serializable and return it as a response to the client 
    return JSONResponse(content=jsonable_encoder(my_cv))



                


