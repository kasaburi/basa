import os
from dotenv import load_dotenv

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base


load_dotenv()


DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("DATABASE_URL is not set")

print("DATABASE EXISTS:", bool(DATABASE_URL))

before_at = DATABASE_URL.split("@")[0]
after_at = DATABASE_URL.split("@")[1]

print("DB BEFORE @:")
print(before_at[:60])

print("DB HOST:")
print(after_at)


if not DATABASE_URL:
    raise ValueError("DATABASE_URL is not set")


# არ დაბეჭდო სრული URL
print("Database connected")


engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    pool_recycle=300,
    pool_size=5,
    max_overflow=10,
)


SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)


Base = declarative_base()



def get_db():

    db = SessionLocal()

    try:

        print("DATABASE SESSION OPEN")

        yield db

    except Exception as e:

        print("DATABASE ERROR:", e)
        raise

    finally:

        print("DATABASE SESSION CLOSE")
        db.close()