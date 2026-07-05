from database import SessionLocal
from models import City

db = SessionLocal()

try:
    db.query(City).delete(synchronize_session=False)
    db.commit()
    print("Cities cleared!")
except Exception as e:
    db.rollback()
    print("Error:", e)
finally:
    db.close()