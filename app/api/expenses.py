from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..schemas.expense import ExpenseCreate, ExpenseOut, ExpenseUpdate, ExpenseReplace, ExpenseSummary, MonthlyExpenseSummary, CategoryExpenseSummary
from ..services import expense_service
from ..dependencies import get_db, get_current_user
from datetime import datetime, time, date
from typing import List

router = APIRouter(prefix="/expenses", tags=["expenses"])

@router.post("/", response_model=ExpenseOut)
def create(exp_in: ExpenseCreate,
           db: Session = Depends(get_db),
           current_user=Depends(get_current_user)):
    return expense_service.create_expense(db, current_user.id, exp_in)

@router.get("/", response_model=List[ExpenseOut])
def list(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    return expense_service.list_expenses(db, current_user.id, skip, limit)

@router.patch("/{expense_id}", response_model=ExpenseOut)
def update(
    expense_id: int,
    exp_in: ExpenseUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    return expense_service.update_expense(db, current_user.id, expense_id, exp_in)

@router.delete("/{expense_id}", status_code=204)
def delete(
    expense_id: int,
    db=Depends(get_db),
    current_user=Depends(get_current_user)
):
    expense_service.delete_expense(db, current_user.id, expense_id)

@router.put("/{expense_id}", response_model=ExpenseOut)
def replace_expense(
    expense_id: int,
    exp_in: ExpenseReplace,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    return expense_service.replace_expense(db, current_user.id, expense_id, exp_in)

@router.get("/summary", response_model=ExpenseSummary)
def expense_summary(
    from_date: date,
    to_date: date,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    return expense_service.expense_summary(db, current_user.id, from_date, to_date) 

@router.get("/summary/monthly", response_model=List[MonthlyExpenseSummary])
def monthly_expense_summary(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    return expense_service.monthly_summary(db, current_user.id)

@router.get("/summary/category", response_model=List[CategoryExpenseSummary])
def category_expense_summary(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    return expense_service.category_summary(db, current_user.id)