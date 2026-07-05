from database import SessionLocal
from models import City

cities = [
    "თბილისი", "ბათუმი", "ქუთაისი", "მცხეთა", "რუსთავი",
    "გორი", "ზუგდიდი", "ფოთი", "სამტრედია", "ახალციხე",
    "ოზურგეთი", "სენაკი", "ხაშური", "თელავი", "ბორჯომი"
]

db = SessionLocal()

try:
    existing = {
        c.name for c in db.query(City.name).all()
    }

    new_cities = [
        City(name=name)
        for name in cities
        if name not in existing
    ]

    db.add_all(new_cities)
    db.commit()

    print(f"{len(new_cities)} cities added!")
except Exception as e:
    db.rollback()
    print("Error:", e)
finally:
    db.close()