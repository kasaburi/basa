from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func

from database import get_db
from models import Report, Category, City







router = APIRouter(
    prefix="/statistics",
    tags=["Statistics"]
)


# საერთო სტატისტიკა
@router.get("/summary")
def get_summary(db: Session = Depends(get_db)):

    total_reports = db.query(Report).count()

    solved = db.query(Report).filter(
        Report.status == "solved"
    ).count()

    pending = db.query(Report).filter(
        Report.status == "pending"
    ).count()

    in_progress = db.query(Report).filter(
        Report.status == "in_progress"
    ).count()

    return {
        "total_reports": total_reports,
        "solved": solved,
        "pending": pending,
        "in_progress": in_progress
    }


# კატეგორიების სტატისტიკა
@router.get("/categories")
def get_categories(db: Session = Depends(get_db)):

    result = (
        db.query(
            Category.name,
            func.count(Report.id)
        )
        .join(
            Report,
            Report.category_id == Category.id
        )
        .group_by(Category.name)
        .all()
    )

    return [
        {
            "category": row[0],
            "count": row[1]
        }
        for row in result
    ]


# ქალაქების სტატისტიკა
@router.get("/cities")
def get_cities(db: Session = Depends(get_db)):

    result = (
        db.query(
            City.name,
            func.count(Report.id)
        )
        .join(
            Report,
            Report.city_id == City.id
        )
        .group_by(City.name)
        .all()
    )

    return [
        {
            "city": row[0],
            "reports": row[1]
        }
        for row in result
    ]