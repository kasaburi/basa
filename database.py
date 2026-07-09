import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# load .env file (local development)
load_dotenv()

# get DATABASE_URL from environment (Render or local)
DATABASE_URL = os.getenv("DATABASE_URL")

# safety check
if not DATABASE_URL:
    raise ValueError("DATABASE_URL is not set")

# create engine
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True
)

# session factory
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# base model
Base = declarative_base()