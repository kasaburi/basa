from fastapi import APIRouter, Depends, Form, UploadFile, File, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import or_
from typing import Optional

import cloudinary.uploader

from models import (
    Report,
    Category,
    ReportStatusHistory,
    User
)

from auth import (
    get_db,
    get_current_user,
    admin_required
)

from ai_service import suggest_category
from services.translator import translate_text


router = APIRouter(
    prefix="/reports",
    tags=["Reports"]
)





# =========================
# CREATE REPORT
# =========================

@router.post("/")
def create_report(

    title_ka: str = Form(...),

    description_ka: str = Form(...),

    city_id: int = Form(...),

    category_id: Optional[int] = Form(None),

    latitude: Optional[float] = Form(None),

    longitude: Optional[float] = Form(None),

    file: UploadFile = File(None),

    db: Session = Depends(get_db),

    current_user: User = Depends(get_current_user)

):


    image_url = None



    # CLOUDINARY UPLOAD

    if file:

        try:

            result = cloudinary.uploader.upload(
                file.file,
                folder="fix-georgia"
            )

            image_url = result["secure_url"]


        except Exception:

            raise HTTPException(
                status_code=500,
                detail="Image upload failed"
            )





    # AI CATEGORY

    final_category = category_id


    if final_category is None:

        final_category = suggest_category(
            title_ka + " " + description_ka
        )





    # TRANSLATION

    try:

        title_en = translate_text(title_ka)

        description_en = translate_text(description_ka)


    except Exception:

        title_en = title_ka

        description_en = description_ka





    report = Report(

        title=title_ka,

        description=description_ka,


        title_ka=title_ka,

        title_en=title_en,


        description_ka=description_ka,

        description_en=description_en,


        city_id=city_id,

        category_id=final_category,

        user_id=current_user.id,


        latitude=latitude,

        longitude=longitude,


        image_url=image_url,


        status="pending"

    )



    try:

        db.add(report)

        db.commit()

        db.refresh(report)


    except Exception:

        db.rollback()

        raise HTTPException(
            status_code=500,
            detail="Report creation failed"
        )



    return {

        "message": "Report created",

        "id": report.id,

        "status": report.status

    }







# =========================
# SOLVE REPORT (ADMIN ONLY)
# =========================

@router.patch("/{report_id}/solve")
def solve_report(

    report_id: int,

    db: Session = Depends(get_db),

    admin: User = Depends(admin_required)

):


    report = (
        db.query(Report)
        .filter(
            Report.id == report_id,
            Report.is_deleted == False
        )
        .first()
    )



    if not report:

        raise HTTPException(
            status_code=404,
            detail="Report not found"
        )



    report.status = "solved"



    history = ReportStatusHistory(

        report_id=report_id,

        status="solved"

    )


    db.add(history)

    db.commit()



    return {

        "message": "Report solved",

        "status": report.status

    }







# =========================
# UPDATE STATUS ADMIN ONLY
# =========================

@router.patch("/{report_id}/status")
def update_status(

    report_id: int,

    status: str,

    db: Session = Depends(get_db),

    admin: User = Depends(admin_required)

):


    report = (
        db.query(Report)
        .filter(
            Report.id == report_id,
            Report.is_deleted == False
        )
        .first()
    )


    if not report:

        raise HTTPException(
            status_code=404,
            detail="Report not found"
        )



    report.status = status



    history = ReportStatusHistory(

        report_id=report_id,

        status=status

    )


    db.add(history)

    db.commit()



    return {

        "message": "Status updated",

        "status": status

    }







# =========================
# STATISTICS
# =========================
@router.get("/stats/overview")
def stats_overview(

    db: Session = Depends(get_db)

):

    # ყველა report ითვლება სტატისტიკაში
    base = db.query(Report)


    return {

        "total": base.count(),


        "pending":
            base.filter(
                Report.status == "pending"
            ).count(),


        "in_progress":
            base.filter(
                Report.status == "in_progress"
            ).count(),


        "solved":
            base.filter(
                Report.status == "solved"
            ).count()

    }




@router.get("/stats/by-category")
def stats_by_category(

    db: Session = Depends(get_db)

):

    categories = db.query(Category).all()


    return [

        {

            "category": category.name,


            "total":
                db.query(Report)
                .filter(
                    Report.category_id == category.id
                )
                .count()

        }

        for category in categories

    ]






# =========================
# DELETE REPORT ADMIN ONLY
# =========================

@router.delete("/{report_id}")
def delete_report(

    report_id: int,

    db: Session = Depends(get_db),

    admin: User = Depends(admin_required)

):


    report = (
        db.query(Report)
        .filter(
            Report.id == report_id
        )
        .first()
    )


    if not report:

        raise HTTPException(
            status_code=404,
            detail="Report not found"
        )



    report.is_deleted = True
    report.deleted_by = admin.id

    db.commit()



    return {

        "message": "Report archived"

    }







# =========================
# FILTER
# =========================

@router.get("/filter")
def filter_reports(

    city_id: Optional[int] = None,

    category_id: Optional[int] = None,

    status: Optional[str] = None,

    search: Optional[str] = None,

    sort: str = "newest",

    page: int = 1,

    limit: int = 100,


    db: Session = Depends(get_db)

):


    page = max(page, 1)

    limit = min(max(limit, 1), 100)



    query = db.query(Report).filter(
        Report.is_deleted == False
    )



    if city_id:

        query = query.filter(
            Report.city_id == city_id
        )


    if category_id:

        query = query.filter(
            Report.category_id == category_id
        )



    if status:

        query = query.filter(
            Report.status == status
        )



    if search:


        search = search.strip()


        query = query.filter(

            or_(

                Report.title.ilike(
                    f"%{search}%"
                ),

                Report.description.ilike(
                    f"%{search}%"
                ),


                Report.title_ka.ilike(
                    f"%{search}%"
                ),

                Report.description_ka.ilike(
                    f"%{search}%"
                ),


                Report.title_en.ilike(
                    f"%{search}%"
                ),

                Report.description_en.ilike(
                    f"%{search}%"
                )

            )

        )



    if sort == "oldest":

        query = query.order_by(
            Report.created_at.asc()
        )

    else:

        query = query.order_by(
            Report.created_at.desc()
        )



    total = query.count()



    reports = (

        query

        .offset(
            (page - 1) * limit
        )

        .limit(limit)

        .all()

    )



    return {

        "success": True,

        "total": total,

        "page": page,

        "limit": limit,

        "data": reports

    }