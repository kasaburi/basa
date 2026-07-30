import os

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pwdlib import PasswordHash
from pydantic import BaseModel, EmailStr

from google.oauth2 import id_token
from google.auth.transport import requests
from sqlalchemy import func
from dotenv import load_dotenv

from database import SessionLocal
from models import User

from auth import create_access_token


load_dotenv()



router = APIRouter(
    prefix="/auth",
    tags=["Auth"]
)



password_hash = PasswordHash.recommended()



GOOGLE_CLIENT_ID = os.getenv(
    "GOOGLE_CLIENT_ID"
)



# DATABASE

def get_db():

    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()


class RegisterRequest(BaseModel):

    name: str
    email: EmailStr
    password: str




class LoginRequest(BaseModel):

    email: EmailStr
    password: str




class GoogleLoginRequest(BaseModel):

    token: str



@router.post("/register")
def register(
    data: RegisterRequest,
    db: Session = Depends(get_db)
):

    existing_user = (
        db.query(User)
        .filter(User.email == data.email)
        .first()
    )

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Email already exists"
        )


    if len(data.password) < 6:
        raise HTTPException(
            status_code=400,
            detail="Password must be at least 6 characters"
        )


    hashed_password = password_hash.hash(
        data.password
    )


    new_user = User(
        name=data.name,
        email=data.email,
        password=hashed_password,
        role="user"
    )


    try:

        db.add(new_user)
        db.commit()
        db.refresh(new_user)


    except Exception:

        db.rollback()

        raise HTTPException(
            status_code=500,
            detail="Registration failed"
        )


    token = create_access_token(
        {
            "user_id": new_user.id,
            "role": new_user.role
        }
    )


    return {

        "access_token": token,

        "token_type": "bearer",

        "user": {

            "id": new_user.id,

            "name": new_user.name,

            "email": new_user.email,

            "role": new_user.role

        }

    }


@router.post("/login")
def login(
    data: LoginRequest,
    db: Session = Depends(get_db)
):

    email = data.email.strip().lower()


    user = (
        db.query(User)
        .filter(
            func.lower(User.email) == email
        )
        .first()
    )


    if not user:
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )


    try:

        password_correct = password_hash.verify(
            data.password,
            user.password
        )

    except Exception:

        password_correct = False



    if not password_correct:

        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )


    token = create_access_token(
        {
            "user_id": user.id,
            "role": user.role
        }
    )


    return {

        "access_token": token,

        "token_type": "bearer",

        "user": {

            "id": user.id,

            "name": user.name,

            "email": user.email,

            "role": user.role

        }

    
    
    }