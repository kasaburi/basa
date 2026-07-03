from database import SessionLocal
from models import Category

db = SessionLocal()

categories = [
    "დაზიანებული გზები",
    "გაუმართავი განათება",
    "ნაგვის დაგროვება",
    "დაზიანებული სკვერები",
    "წყლის გაჟონვა",
    "საგზაო ნიშნები"
]

for name in categories:
    exists = db.query(Category).filter(Category.name == name).first()

    if not exists:
        db.add(Category(name=name))

db.commit()
db.close()

print("Categories seeded safely!")
