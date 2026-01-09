from sqlalchemy.orm import Session
from app.auth import create_keycloak_user
from app.models.user import User
from app.schemas.user import UserCreate

async def signup_user(db: Session, user: UserCreate):
    kc_user_id = await create_keycloak_user(user)

    try:
        db_user = User(
            keycloak_id=kc_user_id,
            name=user.name,
            email=user.email,
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user

    except Exception:
        # rollback DB and optionally delete KC user
        db.rollback()
        raise


def create_user(db: Session, user: UserCreate):
    db_user = User(name=user.name, email=user.email)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_users(db: Session):
    return db.query(User).all()

def get_user_by_id(db: Session, id: str):
    return db.query(User).filter(User.keycloak_id == id).all()