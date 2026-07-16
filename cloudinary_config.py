import cloudinary
import os
from dotenv import load_dotenv

load_dotenv()

CLOUDINARY_CLOUD_NAME = os.getenv("CLOUDINARY_CLOUD_NAME")
CLOUDINARY_API_KEY = os.getenv("CLOUDINARY_API_KEY")
CLOUDINARY_API_SECRET = os.getenv("CLOUDINARY_API_SECRET")

print("Cloudinary Cloud Name:", CLOUDINARY_CLOUD_NAME)
print("Cloudinary API Key exists:", bool(CLOUDINARY_API_KEY))
print("Cloudinary Secret exists:", bool(CLOUDINARY_API_SECRET))

cloudinary.config(
    cloud_name=CLOUDINARY_CLOUD_NAME,
    api_key=CLOUDINARY_API_KEY,
    api_secret=CLOUDINARY_API_SECRET
)