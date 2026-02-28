from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from .db.database import SessionLocal
from .core import security
from .db import models

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exc = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = security.decode_token(token)
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exc
    except Exception:
        raise credentials_exc
    user = db.query(models.User).filter(models.User.email == email).first()
    if user is None:
        raise credentials_exc
    return user