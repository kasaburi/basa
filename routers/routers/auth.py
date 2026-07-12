import os

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from pydantic import BaseModel, EmailStr

from google.oauth2 import id_token
from google.auth.transport import requests

from database import SessionLocal
from models import User
from auth import create_access_token










router = APIRouter(prefix="/auth", tags=["Auth"])

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)

GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")


# ---------------- DB ----------------

def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


# ---------------- SCHEMAS ----------------

class RegisterRequest(BaseModel):
    name: str
    email: EmailStr
    password: str


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class GoogleLoginRequest(BaseModel):
    token: str


# ---------------- REGISTER ----------------

@router.post("/register")
def register(
    data: RegisterRequest,
    db: Session = Depends(get_db)
):

    user = (
        db.query(User)
        .filter(User.email == data.email)
        .first()
    )

    if user:
        raise HTTPException(
            status_code=400,
            detail="Email already exists"
        )

    hashed_password = pwd_context.hash(data.password)

    new_user = User(
        name=data.name,
        email=data.email,
        password=hashed_password
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    token = create_access_token({
        "user_id": new_user.id
    })

    return {
        "access_token": token,
        "token_type": "bearer",
        "user": {
            "id": new_user.id,
            "name": new_user.name,
            "email": new_user.email
        }
    }


# ---------------- LOGIN ----------------

@router.post("/login")
def login(
    data: LoginRequest,
    db: Session = Depends(get_db)
):

    user = (
        db.query(User)
        .filter(User.email == data.email)
        .first()
    )

    if not user:
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    if user.password == "google_oauth":
        raise HTTPException(
            status_code=401,
            detail="Please login with Google"
        )

    if not pwd_context.verify(
        data.password,
        user.password
    ):
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    token = create_access_token({
        "user_id": user.id
    })

    return {
        "access_token": token,
        "token_type": "bearer",
        "user": {
            "id": user.id,
            "name": user.name,
            "email": user.email
        }
    }


# ---------------- GOOGLE LOGIN ----------------

@router.post("/google")
def google_login(
    data: GoogleLoginRequest,
    db: Session = Depends(get_db)
):

    try:

        google_user = id_token.verify_oauth2_token(
            data.token,
            requests.Request(),
            GOOGLE_CLIENT_ID
        )

    except ValueError:

        raise HTTPException(
            status_code=401,
            detail="Invalid Google token"
        )


    email = google_user.get("email")
    name = google_user.get("name")


    if not email:
        raise HTTPException(
            status_code=400,
            detail="Google email not found"
        )


    user = (
        db.query(User)
        .filter(User.email == email)
        .first()
    )


    if not user:

        user = User(
            name=name,
            email=email,
            password="google_oauth"
        )

        db.add(user)
        db.commit()
        db.refresh(user)


    token = create_access_token({
        "user_id": user.id
    })


    return {
        "access_token": token,
        "token_type": "bearer",
        "user": {
            "id": user.id,
            "name": user.name,
            "email": user.email
        }
    }