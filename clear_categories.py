from database import SessionLocal
from models import Category

db = SessionLocal()

try:
    db.query(Category).delete(synchronize_session=False)
    db.commit()
    print("Categories cleared!")
except Exception as e:
    db.rollback()
    print("Error:", e)
finally:
    db.close()