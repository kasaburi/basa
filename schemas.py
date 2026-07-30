from pydantic import BaseModel
from typing import Optional
from datetime import datetime



# =========================
# CATEGORY
# =========================




class CategoryCreate(BaseModel):

    name_ka: str
    name_en: str | None = None



class CategoryResponse(BaseModel):

    id: int
    name_ka: str
    name_en: str | None = None


    class Config:
        from_attributes = True


# =========================
# CITY
# =========================

class CityCreate(BaseModel):
    name_ka: str
    name_en: str | None = None


class CityResponse(BaseModel):
    id: int
    name_ka: str
    name_en: str | None = None

    class Config:
        from_attributes = True






# =========================
# REPORT CREATE
# =========================

class ReportCreate(BaseModel):

    title_ka: str

    title_en: Optional[str] = None


    description_ka: str

    description_en: Optional[str] = None


    city_id: int

    category_id: int


    image_url: Optional[str] = None


    latitude: Optional[float] = None

    longitude: Optional[float] = None





# =========================
# REPORT RESPONSE
# =========================

class ReportResponse(BaseModel):

    id: int


    title_ka: str

    title_en: Optional[str] = None


    description_ka: str

    description_en: Optional[str] = None



    city_id: int

    category_id: int

    user_id: int



    image_url: Optional[str] = None


    latitude: Optional[float] = None

    longitude: Optional[float] = None



    status: str


    is_deleted: bool


    created_at: datetime

    updated_at: datetime



    class Config:

        from_attributes = True