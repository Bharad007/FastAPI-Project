from sqlalchemy.orm import Session
from ..db import models
from ..schemas.expense import ExpenseCreate
import fastapi as FastAPI
from fastapi import HTTPException

def create_expense(db: Session, user_id: int, exp_in: ExpenseCreate) -> models.Expense:
    expense = models.Expense(user_id=user_id, **exp_in.dict())
    db.add(expense)
    db.commit()
    db.refresh(expense)
    return expense

def list_expenses(db: Session, user_id: int, skip: int, limit: int):
    return (
        db.query(models.Expense)
        .filter(models.Expense.user_id == user_id)
        .offset(skip)
        .limit(limit)
        .all()
    )

def update_expense(db: Session, user_id: int, exp_id: int, exp_in):
    expense = (
        db.query(models.Expense)
        .filter(models.Expense.id == exp_id)
        .first()
    )
    if not expense or expense.user_id != user_id:
        raise HTTPException(status_code=404, detail="Expense not found")
    
    if exp_in.amount is not None:
        expense.amount = exp_in.amount
    if exp_in.description is not None:
        expense.description = exp_in.description
    db.commit()
    db.refresh(expense)
    return expense

def delete_expense(db: Session, user_id: int, exp_id: int):
    expense = (
        db.query(models.Expense)
        .filter(models.Expense.id == exp_id)
        .first()
    )
    if not expense or expense.user_id != user_id:
        raise HTTPException(status_code=404, detail="Expense not found")
    
    db.delete(expense)
    db.commit()