from pydantic import BaseModel, field_validator
from datetime import datetime
from typing import Literal
from pycountry import currencies

VALID_CURRENCIES = frozenset(c.alpha_3 for c in currencies)

class Transaction(BaseModel):
    transaction_id: str
    card_id: str
    amount: float
    currency: str
    merchant_id: str
    transaction_type: Literal["PURCHASE", "WITHDRAWAL", "TRANSFER"]
    location: str
    timestamp: datetime

    @field_validator('amount')
    def amount_must_be_positive(cls, v):
        if v <= 0:
            raise ValueError('amount must be positive')
        return v

    @field_validator('currency')
    def validate_currency(cls, v):
        if v not in VALID_CURRENCIES:
            raise ValueError(f'Invalid currency code: {v}')
        return v