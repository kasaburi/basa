from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import SessionLocal
from models import City
from schemas import CityCreate, CityResponse

router = APIRouter(prefix="/cities", tags=["Cities"])


# DB connection
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# GET ALL CITIES
@router.get("/", response_model=list[CityResponse])
def get_cities(db: Session = Depends(get_db)):
    return db.query(City).all()


# CREATE CITY
@router.post("/", response_model=CityResponse)
def create_city(city: CityCreate, db: Session = Depends(get_db)):

    existing_city = db.query(City).filter(
        City.name_ka == city.name_ka
    ).first()

    if existing_city:
        raise HTTPException(
            status_code=400,
            detail="City already exists"
        )

    new_city = City(
        name_ka=city.name_ka,
        name_en=city.name_en
    )

    db.add(new_city)
    db.commit()
    db.refresh(new_city)

    return new_city