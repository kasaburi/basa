from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session 
from passlib.context import CryptContext
from database import SessionLocal
from models import User
import httpx
from auth import create_access_token





router = APIRouter(prefix="/auth", tags=["Auth"])

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/register")
def register(name: str, email: str, password: str, db: Session = Depends(get_db)):

    user = db.query(User).filter(User.email == email).first()
    if user:
        raise HTTPException(status_code=400, detail="Email already exists")

    hashed = pwd_context.hash(password)

    new_user = User(
        name=name,
        email=email,
        password=hashed
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"message": "User created"}


# LOGIN
@router.post("/login")
def login(email: str, password: str, db: Session = Depends(get_db)):

    user = db.query(User).filter(User.email == email).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if not pwd_context.verify(password, user.password):
        raise HTTPException(status_code=401, detail="Wrong password")

    token = create_access_token({"user_id": user.id})

    return {
        "access_token": token,
        "token_type": "bearer"
    }














@router.post("/google")
async def google_login(token: str, db: Session = Depends(get_db)):

    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"https://www.googleapis.com/oauth2/v3/tokeninfo?id_token={token}"
        )

    if response.status_code != 200:
        raise HTTPException(status_code=400, detail="Invalid Google token")

    data = response.json()

    email = data.get("email")
    name = data.get("name")

    if not email:
        raise HTTPException(status_code=400, detail="No email from Google")

    user = db.query(User).filter(User.email == email).first()

    # თუ user არ არსებობს → ვქმნით
    if not user:
        user = User(
            name=name,
            email=email,
            password="google_oauth"
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        token = create_access_token({"user_id": user.id})
        token = create_access_token({"user_id": user.id})

        return {
            "access_token": token,
            "token_type": "bearer",
            "user": {
                "id": user.id,
                "name": user.name,
                "email": user.email
            }
        }