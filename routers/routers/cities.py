from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database import SessionLocal
from models import City
from schemas import CityCreate, CityResponse












router = APIRouter(
    prefix="/cities",
    tags=["Cities"]
)

# Database connection
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ყველა ქალაქის ნახვა
@router.get("/", response_model=list[CityResponse])
def get_cities(db: Session = Depends(get_db)):
    return db.query(City).all()


# ახალი ქალაქის დამატება

@router.post("/", response_model=CityResponse)
def create_city(city: CityCreate, db: Session = Depends(get_db)):
    new_city = City(name=city.name)

    db.add(new_city)
    db.commit()
    db.refresh(new_city)

    return new_city
