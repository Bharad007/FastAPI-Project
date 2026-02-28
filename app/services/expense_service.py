from sqlalchemy.orm import Session
from ..db import models
from ..schemas.expense import ExpenseCreate

def create_expense(db: Session, user_id: int, exp_in: ExpenseCreate) -> models.Expense:
    expense = models.Expense(user_id=user_id, **exp_in.dict())
    db.add(expense)
    db.commit()
    db.refresh(expense)
    return expense

def list_expenses(db: Session, user_id: int):
    return db.query(models.Expense).filter(models.Expense.user_id == user_id).all()