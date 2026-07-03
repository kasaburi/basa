from database import SessionLocal
from models import City

db = SessionLocal()

db.query(City).delete()

db.commit()
db.close()

print("Cities cleared!")