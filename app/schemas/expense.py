from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from datetime import date
from ..db.models import ExpenseCategory

# 1
class ExpenseCreate(BaseModel):
    amount: float
    description: str
    category: ExpenseCategory
# 2
class ExpenseOut(ExpenseCreate):
    id: int
    user_id: int
    created_at: Optional[datetime]

    class Config:
        orm_mode = True
# 3
class ExpenseUpdate(BaseModel):
    amount: Optional[float] = None
    description: Optional[str] = None
    category: Optional[ExpenseCategory] = None
# 4
class ExpenseReplace(BaseModel):
    amount: float
    description: str
    category: ExpenseCategory
# 5
class ExpenseSummary(BaseModel):
    total_amount: float
    from_date: date
    to_date: date
# 6
class MonthlyExpenseSummary(BaseModel):
    month: str
    total: float
# 7
class CategoryExpenseSummary(BaseModel):
    category: str
    total: float

class ExpenseResponse(BaseModel):
    total: int
    limit: int
    skip: int       
    data: list[ExpenseOut]