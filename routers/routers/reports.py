from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Optional
from database import SessionLocal
from models import Report
from schemas import ReportCreate, ReportResponse
from sqlalchemy import desc



from fastapi import APIRouter, Depends, HTTPException, UploadFile, File


import os
import uuid
import shutil


router = APIRouter(prefix="/reports", tags=["Reports"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



@router.get("/filter")
def filter_reports(
    city_id: Optional[int] = None,
    category_id: Optional[int] = None,
    status: Optional[str] = None,
    search: Optional[str] = None,
    sort: Optional[str] = "newest",
    page: int = 1,
    limit: int = 5,
    db: Session = Depends(get_db)
):

    query = db.query(Report)

    # filters
    if city_id:
        query = query.filter(Report.city_id == city_id)

    if category_id:
        query = query.filter(Report.category_id == category_id)

    if status:
        query = query.filter(Report.status == status)

    if search:
        query = query.filter(Report.title.contains(search))

    # 🔥 SORTING (NEW PART)
    if sort == "oldest":
        query = query.order_by(Report.created_at.asc())
    else:
        query = query.order_by(Report.created_at.desc())

    # pagination
    total = query.count()
    skip = (page - 1) * limit
    results = query.offset(skip).limit(limit).all()

    return {
        "total": total,
        "page": page,
        "limit": limit,
        "sort": sort,
        "data": results
    }

# UPDATE STATUS
@router.patch("/{report_id}/status")
def update_status(report_id: int, status: str, db: Session = Depends(get_db)):

    report = db.query(Report).filter(Report.id == report_id).first()

    if not report:
        raise HTTPException(status_code=404, detail="Report not found")

    report.status = status
    db.commit()

    return {"message": "Status updated", "new_status": status}







@router.get("/stats")
def get_stats(db: Session = Depends(get_db)):

    total = db.query(Report).count()

    pending = db.query(Report).filter(Report.status == "pending").count()

    in_progress = db.query(Report).filter(Report.status == "in_progress").count()

    solved = db.query(Report).filter(Report.status == "solved").count()

    return {
        "total": total,
        "pending": pending,
        "in_progress": in_progress,
        "solved": solved
    }


@router.post("/upload")
def upload_image(file: UploadFile = File(...)):

    upload_dir = "uploads"
    os.makedirs(upload_dir, exist_ok=True)

    # 🔥 unique filename (production standard)
    file_ext = file.filename.split(".")[-1]
    filename = f"{uuid.uuid4()}.{file_ext}"

    file_path = os.path.join(upload_dir, filename)

    # 💾 save file
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # 🌐 public URL
    file_url = f"/uploads/{filename}"

    return {
        "filename": filename,
        "url": file_url
    }