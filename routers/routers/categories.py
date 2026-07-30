from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm import Session

from database import SessionLocal
from models import Category
from schemas import CategoryCreate, CategoryResponse


router = APIRouter(
    prefix="/categories",
    tags=["Categories"]
)


def get_db():

    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()



# CREATE CATEGORY

@router.post("/", response_model=CategoryResponse)
def create_category(
    category: CategoryCreate,
    db: Session = Depends(get_db)
):

    existing = (
        db.query(Category)
        .filter(
            Category.name_ka == category.name_ka
        )
        .first()
    )


    if existing:

        raise HTTPException(
            status_code=400,
            detail="Category already exists"
        )



    new_category = Category(

        name_ka=category.name_ka,

        name_en=category.name_en

    )


    db.add(new_category)

    db.commit()

    db.refresh(new_category)


    return new_category





# GET ALL CATEGORIES

@router.get("/", response_model=list[CategoryResponse])
def get_categories(
    db: Session = Depends(get_db)
):

    try:

        categories = (
            db.query(Category)
            .all()
        )


        return categories


    except OperationalError:

        raise HTTPException(
            status_code=500,
            detail="Database connection failed"
        )