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