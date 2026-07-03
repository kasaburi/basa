from database import SessionLocal
from models import City

db = SessionLocal()

cities = ["თბილისი", "ბათუმი", "ქუთაისი","მცხეთა", "რუსთავი","გორი", "ზუგდიდი", "ფოთი", "სამტრედია", "ახალციხე", "ოზურგეთი", "სენაკი", "ხაშური", "თელავი", "ბორჯომი"]

for name in cities:
    db.add(City(name=name))

db.commit()
db.close()

print("Cities added!")