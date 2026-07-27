from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from datetime import datetime
from database import Base
from sqlalchemy import Column, Integer, String, Text, ForeignKey, Float, DateTime, Boolean


# USERS
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String, nullable=False)

    email = Column(
        String,
        unique=True,
        index=True,
        nullable=True
    )

    password = Column(String, nullable=False)

    role = Column(String, default="user")

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )

    reports = relationship(
        "Report",
        back_populates="user"
    )
# CITIES
class City(Base):
    __tablename__ = "cities"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)

    reports = relationship("Report", back_populates="city")


# CATEGORIES
class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)

    reports = relationship("Report", back_populates="category")


# REPORTS
class Report(Base):
    __tablename__ = "reports"

    id = Column(Integer, primary_key=True, index=True)

    # ძველი ველები Angular-ისთვის (არ ვშლით)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=False)

    # ახალი თარგმნის ველები
    title_ka = Column(String, nullable=True)
    title_en = Column(String, nullable=True)

    description_ka = Column(Text, nullable=True)
    description_en = Column(Text, nullable=True)

    image_url = Column(String, nullable=True)

    city_id = Column(Integer, ForeignKey("cities.id"))
    category_id = Column(Integer, ForeignKey("categories.id"))
    user_id = Column(Integer, ForeignKey("users.id"))

    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)

    status = Column(String, default="pending")

    is_deleted = Column(Boolean, default=False)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    user = relationship("User", back_populates="reports")
    city = relationship("City", back_populates="reports")
    category = relationship("Category", back_populates="reports")

    status_history = relationship("ReportStatusHistory", back_populates="report")
    ratings = relationship("Rating", back_populates="report")


# STATUS HISTORY
class ReportStatusHistory(Base):
    __tablename__ = "report_status_history"

    id = Column(Integer, primary_key=True, index=True)

    report_id = Column(Integer, ForeignKey("reports.id"))

    status = Column(String)

    changed_at = Column(
        DateTime,
        default=datetime.utcnow
    )

    report = relationship(
        "Report",
        back_populates="status_history"
    )



# RATINGS
class Rating(Base):
    __tablename__ = "ratings"

    id = Column(Integer, primary_key=True, index=True)

    report_id = Column(Integer, ForeignKey("reports.id"))

    user_id = Column(Integer, ForeignKey("users.id"))

    rating = Column(Integer)

    comment = Column(Text, nullable=True)

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )

    report = relationship(
        "Report",
        back_populates="ratings"
    )

    user = relationship("User")