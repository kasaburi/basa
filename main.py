from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

from database import Base, engine, SessionLocal
import models
from routers.routers import statistics

from routers.routers.cities import router as cities_router
from routers.routers.categories import router as categories_router
from routers.routers.reports import router as reports_router
from routers.routers.auth import router as auth_router

import os


app = FastAPI()
app.include_router(statistics.router)
# DB init
Base.metadata.create_all(bind=engine)

# uploads folder fix
if not os.path.exists("uploads"):
    os.makedirs("uploads")

app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# DB dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ROUTERS
app.include_router(auth_router)
app.include_router(cities_router)
app.include_router(categories_router)
app.include_router(reports_router)

# ROOT
@app.get("/")
def home():
    return {"message": "Fix Georgia API running"}