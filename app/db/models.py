from sqlalchemy import Column, Integer, String, DateTime, Float, Enum, ForeignKey
from datetime import datetime
from .database import Base
from enum import Enum as PyEnum

class ExpenseCategory(str, PyEnum):
    food = "food"
    transport = "transport"
    rent = "rent"
    entertainment = "entertainment"
    utilities = "utilities"
    other = "other"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)        # auto‑increment id
    email = Column(String, unique=True, index=True)
    password = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)

class Expense(Base):
    __tablename__ = "expenses"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), index=True)  # FK to users.id
    amount = Column(Float)
    description = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    category = Column(Enum(ExpenseCategory), nullable=False)