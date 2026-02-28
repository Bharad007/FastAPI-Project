from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..schemas.expense import ExpenseCreate, ExpenseOut
from ..services import expense_service
from ..dependencies import get_db, get_current_user

router = APIRouter(prefix="/expenses", tags=["expenses"])

@router.post("/", response_model=ExpenseOut)
def create(exp_in: ExpenseCreate,
           db: Session = Depends(get_db),
           current_user=Depends(get_current_user)):
    return expense_service.create_expense(db, current_user.id, exp_in)

@router.get("/", response_model=list[ExpenseOut])
def list(db: Session = Depends(get_db),
         current_user=Depends(get_current_user)):
    return expense_service.list_expenses(db, current_user.id)