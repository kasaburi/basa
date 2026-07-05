from database import SessionLocal
from models import City

db = SessionLocal()

cities = [
    "თბილისი", "ბათუმი", "ქუთაისი", "მცხეთა", "რუსთავი",
    "გორი", "ზუგდიდი", "ფოთი", "სამტრედია", "ახალციხე",
    "ოზურგეთი", "სენაკი", "ხაშური", "თელავი", "ბორჯომი"
]

try:
    for name in cities:
        # optional: duplicate check (ძალიან რეკომენდებულია)
        exists = db.query(City).filter(City.name == name).first()
        if not exists:
            db.add(City(name=name))

    db.commit()
    print("Cities added!")
except Exception as e:
    db.rollback()
    print("Error:", e)
finally:
    db.close()