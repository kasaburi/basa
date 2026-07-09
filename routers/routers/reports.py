from fastapi import APIRouter, Depends, Form, UploadFile, File, HTTPException
from sqlalchemy.orm import Session
from typing import Optional
import os
import uuid
import shutil

from database import SessionLocal
from models import Report, Category, ReportStatusHistory
from ai_service import suggest_category


router = APIRouter(prefix="/reports", tags=["Reports"])


# ---------------------------
# DB DEPENDENCY
# ---------------------------
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()




@router.post("/")
def create_report(
    title: str = Form(...),
    description: str = Form(...),
    city_id: int = Form(...),
    category_id: int = Form(...),   # დაამატე აქ
    user_id: Optional[int] = Form(None),
    latitude: Optional[float] = Form(None),
    longitude: Optional[float] = Form(None),
    file: UploadFile = File(None),
    db: Session = Depends(get_db)
):






    # 1. AI CATEGORY
  

    # 2. IMAGE UPLOAD
    image_url = None

    if file:
        upload_dir = "uploads"
        os.makedirs(upload_dir, exist_ok=True)

        ext = file.filename.split(".")[-1]
        filename = f"{uuid.uuid4()}.{ext}"
        path = os.path.join(upload_dir, filename)

        with open(path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        image_url = f"/uploads/{filename}"

    # 3. SAVE REPORT
    new_report = Report(
        title=title,
        description=description,
        city_id=city_id,
        category_id=category_id,
        user_id=user_id,
        latitude=latitude,
        longitude=longitude,
        image_url=image_url,
        status="pending"
    )





    db.add(new_report)
    db.commit()
    db.refresh(new_report)

    return {
        "message": "Report created",
        "report": new_report
    }


# ---------------------------
# FILTER REPORTS
# ---------------------------
@router.get("/filter")
def filter_reports(
    city_id: Optional[int] = None,
    category_id: Optional[int] = None,
    status: Optional[str] = None,
    search: Optional[str] = None,
    sort: str = "newest",
    page: int = 1,
    limit: int = 5,
    db: Session = Depends(get_db)
):

    query = db.query(Report)

    if city_id:
        query = query.filter(Report.city_id == city_id)

    if category_id:
        query = query.filter(Report.category_id == category_id)

    if status:
        query = query.filter(Report.status == status)

    if search:
        query = query.filter(Report.title.contains(search))

    if sort == "oldest":
        query = query.order_by(Report.created_at.asc())
    else:
        query = query.order_by(Report.created_at.desc())

    total = query.count()
    results = query.offset((page - 1) * limit).limit(limit).all()

    return {
        "total": total,
        "page": page,
        "limit": limit,
        "data": results
    }


# ---------------------------
# UPDATE STATUS + HISTORY
# ---------------------------
@router.patch("/{report_id}/status")
def update_status(report_id: int, status: str, db: Session = Depends(get_db)):

    report = db.query(Report).filter(Report.id == report_id).first()

    if not report:
        raise HTTPException(status_code=404, detail="Report not found")

    report.status = status

    history = ReportStatusHistory(
        report_id=report_id,
        status=status
    )

    db.add(history)
    db.commit()

    return {"message": "Status updated", "status": status}


# ---------------------------
# STATS OVERVIEW
# ---------------------------
@router.get("/stats/overview")
def stats_overview(db: Session = Depends(get_db)):

    return {
        "total": db.query(Report).count(),
        "pending": db.query(Report).filter(Report.status == "pending").count(),
        "in_progress": db.query(Report).filter(Report.status == "in_progress").count(),
        "solved": db.query(Report).filter(Report.status == "solved").count()
    }


# ---------------------------
# STATS BY CATEGORY
# ---------------------------
@router.get("/stats/by-category")
def stats_by_category(db: Session = Depends(get_db)):

    categories = db.query(Category).all()

    return [
        {
            "category": c.name,
            "total": db.query(Report).filter(Report.category_id == c.id).count()
        }
        for c in categories
    ]


# ---------------------------
# IMAGE UPLOAD ONLY
# ---------------------------
@router.post("/upload")
def upload_image(file: UploadFile = File(...)):

    upload_dir = "uploads"
    os.makedirs(upload_dir, exist_ok=True)

    ext = file.filename.split(".")[-1]
    filename = f"{uuid.uuid4()}.{ext}"
    path = os.path.join(upload_dir, filename)

    with open(path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return {
        "url": f"/uploads/{filename}"
    }