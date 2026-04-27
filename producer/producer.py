import random
import uuid
from datetime import datetime
from typing import Literal, cast
from faker import Faker
from producer.models import Transaction, VALID_CURRENCIES

# Alias del Literal definido en models.py para el type checker
TransactionType = Literal["PURCHASE", "WITHDRAWAL", "TRANSFER"]

# Instancia global reutilizable de Faker para generar datos sintéticos
fake = Faker()


def generate_transaction() -> Transaction:
    """Genera una transacción sintética con datos aleatorios válidos."""
    transaction_id = str(uuid.uuid4())
    card_id = f"CARD{random.randint(100000, 999999)}"
    merchant_id = f"MERCH{random.randint(1000, 9999)}"
    amount = round(random.uniform(1, 10000), 2)

    # VALID_CURRENCIES viene de pycountry vía models.py, cubre todos los códigos ISO 4217
    currency = random.choice(list(VALID_CURRENCIES))

    # cast() solo informa al type checker; random.choice devuelve str en runtime
    transaction_type = cast(TransactionType, random.choice(["PURCHASE", "WITHDRAWAL", "TRANSFER"]))

    location = fake.city()
    timestamp = datetime.now()

    return Transaction(
        transaction_id=transaction_id,
        card_id=card_id,
        amount=amount,
        currency=currency,
        merchant_id=merchant_id,
        transaction_type=transaction_type,
        location=location,
        timestamp=timestamp
    )