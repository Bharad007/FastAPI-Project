from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class ExpenseCreate(BaseModel):
    amount: float
    description: str

class ExpenseOut(ExpenseCreate):
    id: int
    user_id: int
    created_at: Optional[datetime]

    class Config:
        orm_mode = True

class ExpenseUpdate(BaseModel):
    amount: Optional[float] = None
    description: Optional[str] = None

class ExpenseReplace(BaseModel):
    amount: float
    description: str

class ExpenseSummary(BaseModel):
    total_amount: float
    from_date: str
    to_date: str

class MonthlyExpenseSummary(BaseModel):
    month: str
    total: float