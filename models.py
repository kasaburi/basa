from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    ForeignKey,
    Float,
    DateTime,
    Boolean
)

from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from datetime import datetime

from database import Base



# =========================
# USERS
# =========================

class User(Base):

    __tablename__ = "users"


    id = Column(
        Integer,
        primary_key=True,
        index=True
    )


    name = Column(
        String,
        nullable=False
    )


    email = Column(
        String,
        unique=True,
        index=True,
        nullable=False
    )


    password = Column(
        String,
        nullable=False
    )


    role = Column(
        String,
        default="user",
        nullable=False
    )


    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )


    reports = relationship(
        "Report",
        back_populates="user"
    )





# =========================
# CITIES
# =========================
class City(Base):

    __tablename__ = "cities"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    name_ka = Column(
        String,
        nullable=False
    )

    name_en = Column(
        String,
        nullable=True
    )

    reports = relationship(
        "Report",
        back_populates="city"
    )

# =========================
# CATEGORIES
# =========================

class Category(Base):

    __tablename__ = "categories"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    name_ka = Column(
        String,
        unique=True,
        nullable=False
    )

    name_en = Column(
        String,
        nullable=True
    )

    reports = relationship(
        "Report",
        back_populates="category"
    )
# =========================
# REPORTS
# =========================

class Report(Base):

    __tablename__ = "reports"



    id = Column(
        Integer,
        primary_key=True,
        index=True
    )


    # ძველი Angular მხარდაჭერა
    title = Column(
        String,
        nullable=True
    )


    description = Column(
        Text,
        nullable=True
    )



    # MULTILINGUAL

    title_ka = Column(
        String,
        nullable=False
    )


    title_en = Column(
        String,
        nullable=True
    )


    description_ka = Column(
        Text,
        nullable=False
    )


    description_en = Column(
        Text,
        nullable=True
    )



    # IMAGE

    image_url = Column(
        String,
        nullable=True
    )



    # RELATIONS

    city_id = Column(
        Integer,
        ForeignKey("cities.id"),
        nullable=False
    )


    category_id = Column(
        Integer,
        ForeignKey("categories.id"),
        nullable=False
    )


    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False
    )



    # MAP

    latitude = Column(
        Float,
        nullable=True
    )


    longitude = Column(
        Float,
        nullable=True
    )



    # STATUS

    status = Column(
        String,
        default="pending",
        nullable=False
    )



    is_deleted = Column(
        Boolean,
        default=False,
        nullable=False
    )



    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )


    updated_at = Column(
        DateTime,
        default=func.now(),
        onupdate=func.now()
    )



    user = relationship(
        "User",
        back_populates="reports"
    )


    city = relationship(
        "City",
        back_populates="reports"
    )


    category = relationship(
        "Category",
        back_populates="reports"
    )


    status_history = relationship(
        "ReportStatusHistory",
        back_populates="report",
        cascade="all, delete-orphan"
    )


    ratings = relationship(
        "Rating",
        back_populates="report",
        cascade="all, delete-orphan"
    )





# =========================
# STATUS HISTORY
# =========================

class ReportStatusHistory(Base):

    __tablename__ = "report_status_history"


    id = Column(
        Integer,
        primary_key=True,
        index=True
    )


    report_id = Column(
        Integer,
        ForeignKey("reports.id"),
        nullable=False
    )


    status = Column(
        String,
        nullable=False
    )


    changed_at = Column(
        DateTime,
        default=datetime.utcnow
    )


    report = relationship(
        "Report",
        back_populates="status_history"
    )





# =========================
# RATINGS
# =========================

class Rating(Base):

    __tablename__ = "ratings"


    id = Column(
        Integer,
        primary_key=True,
        index=True
    )


    report_id = Column(
        Integer,
        ForeignKey("reports.id"),
        nullable=False
    )


    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False
    )


    rating = Column(
        Integer,
        nullable=False
    )


    comment = Column(
        Text,
        nullable=True
    )


    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )


    report = relationship(
        "Report",
        back_populates="ratings"
    )


    user = relationship(
        "User"
    )