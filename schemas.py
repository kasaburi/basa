from pydantic import BaseModel
from typing import Optional


class CategoryCreate(BaseModel):
    name: str


class CategoryResponse(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True

class Config:
 from_attributes = True


class CityCreate(BaseModel):
    name: str


class CityResponse(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True



class ReportCreate(BaseModel):
    title: str
    description: str
    city_id: int
    category_id: int
    user_id: int
    image_url: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None


class ReportResponse(BaseModel):
    id: int
    title: str
    description: str
    city_id: int
    category_id: int
    user_id: int
    image_url: Optional[str]
    latitude: Optional[float]
    longitude: Optional[float]
    status: str

    class Config:
        from_attributes = True