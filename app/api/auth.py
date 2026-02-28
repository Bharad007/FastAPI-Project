from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..schemas.user import UserCreate, UserOut
from ..services import auth_service
from ..core import security
from ..dependencies import get_db, get_current_user

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register", response_model=UserOut)
def register(user_in: UserCreate, db: Session = Depends(get_db)):
    try:
        user = auth_service.register_user(db, user_in)
    except ValueError:
        raise HTTPException(status_code=409, detail="Email already exists")
    return user

@router.post("/login")
def login(form_data: UserCreate, db: Session = Depends(get_db)):
    user = auth_service.authenticate_user(db, form_data.email, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = security.create_access_token({"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/me", response_model=UserOut)
def me(current_user=Depends(get_current_user)):
    return current_user