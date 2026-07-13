from datetime import datetime, timedelta
import os

from jose import jwt, JWTError
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from dotenv import load_dotenv

from database import SessionLocal
from models import User


load_dotenv()


SECRET_KEY = os.getenv("SECRET_KEY")

if not SECRET_KEY:
    raise Exception("SECRET_KEY is missing in environment variables")


ALGORITHM = "HS256"

ACCESS_TOKEN_EXPIRE_MINUTES = 60



oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/auth/login"
)



# DATABASE

def get_db():

    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()





# CREATE JWT TOKEN

def create_access_token(data: dict):

    to_encode = data.copy()


    expire = datetime.utcnow() + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )


    to_encode.update({
        "exp": expire
    })


    token = jwt.encode(
        to_encode,
        SECRET_KEY,
        algorithm=ALGORITHM
    )


    return token






# CURRENT USER

def get_current_user(

    token: str = Depends(oauth2_scheme),

    db: Session = Depends(get_db)

):

    try:

        payload = jwt.decode(

            token,

            SECRET_KEY,

            algorithms=[ALGORITHM]

        )


        user_id = payload.get("user_id")


        if user_id is None:

            raise HTTPException(
                status_code=401,
                detail="Invalid token"
            )


    except JWTError:

        raise HTTPException(
            status_code=401,
            detail="Invalid token"
        )



    user = (
        db.query(User)
        .filter(User.id == user_id)
        .first()
    )


    if user is None:

        raise HTTPException(
            status_code=404,
            detail="User not found"
        )


    return user