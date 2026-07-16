import cloudinary
import os
from dotenv import load_dotenv

load_dotenv()

CLOUDINARY_CLOUD_NAME = os.getenv("CLOUDINARY_CLOUD_NAME")
CLOUDINARY_API_KEY = os.getenv("CLOUDINARY_API_KEY")
CLOUDINARY_API_SECRET = os.getenv("CLOUDINARY_API_SECRET")

if not CLOUDINARY_CLOUD_NAME:
    raise ValueError("CLOUDINARY_CLOUD_NAME is missing")

if not CLOUDINARY_API_KEY:
    raise ValueError("CLOUDINARY_API_KEY is missing")

if not CLOUDINARY_API_SECRET:
    raise ValueError("CLOUDINARY_API_SECRET is missing")


cloudinary.config(
    cloud_name=CLOUDINARY_CLOUD_NAME,
    api_key=CLOUDINARY_API_KEY,
    api_secret=CLOUDINARY_API_SECRET
)