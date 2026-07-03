from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from database import Base, engine
import models

from routers.routers.cities import router as cities_router
from routers.routers.categories import router as categories_router
from routers.routers.reports import router as reports_router
from routers.routers.auth import router as auth_router   # 👈 დაამატე, თუ auth.py შექმენი




Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(auth_router)        # 👈 დაამატე
app.include_router(cities_router)
app.include_router(categories_router)
app.include_router(reports_router)

app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")


@app.get("/")
def home():
    return {"message": "Fix Georgia API running"}

