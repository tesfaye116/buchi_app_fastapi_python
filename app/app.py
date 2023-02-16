from fastapi import FastAPI

from routes.pets import router as PetsRouter
from routes.customers import router as CustomersRouter
from routes.adopt import router as AdoptsRouter
from routes.report import router as ReportRouter

from fastapi.staticfiles import StaticFiles


app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(PetsRouter, tags=["Pets"], prefix="/api/v1/pets")

app.include_router(CustomersRouter, tags=["Customers"], prefix="/api/v1/customers")

app.include_router(AdoptsRouter, tags=["Adopts"], prefix="/api/v1/adoptions")

app.include_router(ReportRouter, tags=["Report"], prefix="/api/v1/generateReport")


@app.get("/", tags=["Root"])
async def read_root():
    return {"message": "Welcome to Buchi's Pet Adoption API, Made with ❤️ by Tesfaye Girma"}
