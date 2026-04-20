from pydantic import BaseModel, field_validator
from datetime import datetime
from typing import Optional

class LoanRecord(BaseModel):
    loan_id: str
    credit_score: Optional[int]
    loan_amount: float
    origination_date: datetime

    @field_validator('loan_amount')
    def amount_must_be_positive(cls, v):
        if v <= 0:
            raise ValueError('loan_amount must be positive')
        return v