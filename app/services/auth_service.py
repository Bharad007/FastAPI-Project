from sqlalchemy.orm import Session
from ..db import models
from ..core import security
from ..schemas.user import UserCreate

def register_user(db: Session, user_in: UserCreate) -> models.User:
    existing = db.query(models.User).filter(models.User.email == user_in.email).first()
    if existing:
        raise ValueError("email already registered")
    hashed = security.hash_password(user_in.password)
    user = models.User(email=user_in.email, password=hashed)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def authenticate_user(db: Session, email: str, password: str) -> models.User | None:
    user = db.query(models.User).filter(models.User.email == email).first()
    if user and security.verify_password(password, user.password):
        return user
    return None