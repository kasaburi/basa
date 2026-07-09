from database import SessionLocal
from models import City, Category

db = SessionLocal()

# ქალაქებიდან string-ის წაშლა
db.query(City).filter(City.name == "string").delete()

# კატეგორიებიდან string-ის წაშლა
db.query(Category).filter(Category.name == "string").delete()

db.commit()

db.close()

print("Test data deleted")