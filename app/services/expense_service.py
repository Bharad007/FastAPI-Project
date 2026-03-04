from sqlalchemy.orm import Session
from ..db import models
from ..schemas.expense import ExpenseCreate
import fastapi as FastAPI
from fastapi import HTTPException
from sqlalchemy import func
from datetime import datetime, time, date

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
    
    if exp_in.amount is None and exp_in.description is None:
        raise HTTPException(status_code=400, detail="At least one field (amount or description) must be provided for update")
    
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

def replace_expense(db: Session, user_id: int, exp_id: int, exp_in):
    expense = (
        db.query(models.Expense)
        .filter(models.Expense.id == exp_id)
        .first()
    )
    if not expense or expense.user_id != user_id:
        raise HTTPException(status_code=404, detail="Expense not found")
    
    expense.amount = exp_in.amount
    expense.description = exp_in.description
    db.commit()
    db.refresh(expense)
    return expense

def expense_summary(db: Session, user_id: int, from_date: date, to_date: date):
    start_dt = datetime.combine(from_date, time.min)
    end_dt = datetime.combine(to_date, time.max)

    total = (
        db.query(func.sum(models.Expense.amount))
        .filter(
            models.Expense.user_id == user_id,
            models.Expense.created_at >= start_dt,
            models.Expense.created_at <= end_dt
        )
        .scalar()
    )

    return {
        "total_amount": total or 0.0,   
        "from_date": str(from_date),
        "to_date": str(to_date)
    }

def monthly_summary(db: Session, user_id: int):
    results = (
        db.query(
            func.strftime("%Y-%m", models.Expense.created_at).label("month"),
            func.sum(models.Expense.amount).label("total")
        )
        .filter(models.Expense.user_id == user_id)
        .group_by("month")
        .order_by("month")
        .all()
    )

    return [
        {"month": row.month, "total": row.total}
        for row in results
    ]