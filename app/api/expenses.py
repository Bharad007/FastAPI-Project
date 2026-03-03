from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..schemas.expense import ExpenseCreate, ExpenseOut, ExpenseUpdate, ExpenseReplace
from ..services import expense_service
from ..dependencies import get_db, get_current_user

router = APIRouter(prefix="/expenses", tags=["expenses"])

@router.post("/", response_model=ExpenseOut)
def create(exp_in: ExpenseCreate,
           db: Session = Depends(get_db),
           current_user=Depends(get_current_user)):
    return expense_service.create_expense(db, current_user.id, exp_in)

@router.get("/", response_model=list[ExpenseOut])
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