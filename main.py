from fastapi import FastAPI, Depends
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from database import Base, engine, SessionLocal
import models  # აუცილებელია tables რომ შეიქმნას

from routers.routers.cities import router as cities_router
from routers.routers.categories import router as categories_router
from routers.routers.reports import router as reports_router
from routers.routers.auth import router as auth_router


# APP
app = FastAPI()

# DB init (tables create)
Base.metadata.create_all(bind=engine)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# DB dependency (global use)
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


# STATIC FILES
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")


# ROOT
@app.get("/")
def home():
    return {"message": "Fix Georgia API running"}