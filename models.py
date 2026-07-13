from sqlalchemy import Column, Integer, String, Text, ForeignKey, Float, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from datetime import datetime
from database import Base


# USERS



role = Column(String, default="user")
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String, unique=True)
    password = Column(String)
    role = Column(String, default="user")

    reports = relationship("Report", back_populates="user")  
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


# REPORTS (main table)
class Report(Base):
    __tablename__ = "reports"

    id = Column(Integer, primary_key=True, index=True)

    title = Column(String, nullable=False)
    description = Column(Text, nullable=False)
    image_url = Column(String, nullable=True)

    city_id = Column(Integer, ForeignKey("cities.id"))
    category_id = Column(Integer, ForeignKey("categories.id"))
    user_id = Column(Integer, ForeignKey("users.id"))

    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)

    status = Column(String, default="pending")  # pending / in_progress / solved

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    # relationships
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
    changed_at = Column(DateTime, default=datetime.utcnow)

    report = relationship("Report", back_populates="status_history")


# RATINGS
class Rating(Base):
    __tablename__ = "ratings"

    id = Column(Integer, primary_key=True, index=True)

    report_id = Column(Integer, ForeignKey("reports.id"))
    user_id = Column(Integer, ForeignKey("users.id"))

    rating = Column(Integer)  # 1-5
    comment = Column(Text, nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)

    report = relationship("Report", back_populates="ratings")
    user = relationship("User")