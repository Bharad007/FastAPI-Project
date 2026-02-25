
from fastapi import FastAPI, HTTPException
from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import bcrypt
from pydantic import BaseModel

# Database setup
DATABASE_URL = "sqlite:///./expense_tracker.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# User model
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)  
    created_at = Column(DateTime, default=datetime.utcnow)

Base.metadata.create_all(bind=engine)

app = FastAPI()

class RegisterRequest(BaseModel):
    email: str
    password: str

@app.post("/auth/register")
def register(request: RegisterRequest):
    db = SessionLocal()

    try:

        # Check if the email is already registered
        existing_user = db.query(User).filter(User.email == request.email).first()
        if existing_user:
            raise HTTPException(status_code=400, detail="Email already exists")

        #Hash the password
        hashed_password = bcrypt.hashpw(request.password.encode(), bcrypt.gensalt()).decode()
        # Create a new user object
        new_user = User(email=request.email, password=hashed_password)
        # Add the user to the database
        db.add(new_user)        
        db.commit()
        return {"status": "ok", "message": f"User {request.email} registered successfully"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        db.close()