from sqlalchemy.orm import Session

from app.models.user import User
from app.utils.hashing import Hash


def seed_admin(db: Session):

    admin = db.query(User).filter(User.email == "admin@airline.com").first()

    if admin:
        return

    admin = User(
        name="System Admin",
        email="admin@airline.com",
        password=Hash.hash_password("Admin@123"),
        role="Admin",
        is_active=True
    )

    db.add(admin)
    db.commit()

    print("Admin Created Successfully")