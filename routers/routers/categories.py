from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm import Session
from database import SessionLocal
from models import Category
from schemas import CategoryCreate, CategoryResponse

router = APIRouter(prefix="/categories", tags=["Categories"])


# DB dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# CREATE CATEGORY
@router.post("/", response_model=CategoryResponse)
def create_category(category: CategoryCreate, db: Session = Depends(get_db)):

    # optional: duplicate check (ძალიან მნიშვნელოვანია რეალურ პროექტში)
    existing = db.query(Category).filter(Category.name == category.name).first()
    if existing:
        raise HTTPException(status_code=400, detail="Category already exists")

    new_category = Category(name=category.name)

    db.add(new_category)
    db.commit()
    db.refresh(new_category)

    return new_category


# GET ALL CATEGORIES
@router.get("/", response_model=list[CategoryResponse])
def get_categories(db: Session = Depends(get_db)):
    try:
        return db.query(Category).all()

    except OperationalError:
        raise HTTPException(
        status_code=500,
        detail="Database connection failed"
    )