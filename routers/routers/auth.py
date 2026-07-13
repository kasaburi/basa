import os

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pwdlib import PasswordHash
from pydantic import BaseModel, EmailStr

from google.oauth2 import id_token
from google.auth.transport import requests

from database import SessionLocal
from models import User

from auth import create_access_token


router = APIRouter(
    prefix="/auth",
    tags=["Auth"]
)


password_hash = PasswordHash.recommended()


GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")


# DATABASE

def get_db():

    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()



# SCHEMAS

class RegisterRequest(BaseModel):
    name: str
    email: EmailStr
    password: str



class LoginRequest(BaseModel):
    email: EmailStr
    password: str



class GoogleLoginRequest(BaseModel):
    token: str




# REGISTER

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
        password=hashed_password
    )


    db.add(new_user)
    db.commit()
    db.refresh(new_user)


    token = create_access_token(
        {
            "user_id": new_user.id
        }
    )


    return {
        "message": "Registration successful",
        "access_token": token,
        "token_type": "bearer",
        "user": {
            "id": new_user.id,
            "name": new_user.name,
            "email": new_user.email
        }
    }




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

    print("EMAIL:", data.email)
    print("USER:", user)


    if not user:
        raise HTTPException(
            status_code=401,
            detail="User not found"
        )


    password_correct = password_hash.verify(
        data.password,
        user.password
    )


    print("PASSWORD MATCH:", password_correct)


    if not password_correct:
        raise HTTPException(
            status_code=401,
            detail="Wrong password"
        )


    token = create_access_token(
        {
            "user_id": user.id
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






# GOOGLE LOGIN

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
            password=password_hash.hash(
                os.urandom(16).hex()
            )
        )


        db.add(user)
        db.commit()
        db.refresh(user)




    token = create_access_token(
        {
            "user_id": user.id
        }
    )


    return {
        "access_token": token,
        "token_type": "bearer",
        "user": {
            "id": user.id,
            "name": user.name,
            "email": user.email
        }
    }