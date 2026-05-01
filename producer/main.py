from fastapi import FastAPI
from producer.models import Transaction
from producer.producer import generate_transaction
from messaging.kafka_producer import send_transaction
from fastapi import BackgroundTasks
import asyncio
import random

# El producer actúa como API HTTP que otros servicios pueden llamar
# para obtener transacciones sintéticas
app = FastAPI(title="Fraud Detection Producer")


@app.get("/transaction", response_model=Transaction)
def get_transaction() -> Transaction:
    # Cada llamada genera una transacción nueva con datos aleatorios válidos
    transaction = generate_transaction()
    # Envía la transacción al topic de Kafka
    send_transaction(transaction)
    return transaction

@app.post("/simulate-fraud/{card_id}")
def simulate_fraud(card_id: str):
    # Genera 5 transacciones con el mismo card_id
    for _ in range(5):
        transaction = generate_transaction()
        transaction = transaction.model_copy(update={"card_id": card_id})
        send_transaction(transaction)
    return {"message": f"5 transacciones enviadas para {card_id}"}

async def generate_continuous(n: int, delay: float):
    fraud_card = f"CARD{random.randint(100000, 999999)}"
    for i in range(n):
        transaction = generate_transaction()
        # Cada 5 transacciones, usa la misma tarjeta para simular fraude
        if i % 5 == 0:
            transaction = transaction.model_copy(update={"card_id": fraud_card})
        send_transaction(transaction)
        await asyncio.sleep(delay)

@app.post("/start-stream")
async def start_stream(background_tasks: BackgroundTasks, n: int = 100, delay: float = 0.5):
    background_tasks.add_task(generate_continuous, n, delay)
    return {"message": f"Enviando {n} transacciones con {delay}s de intervalo"}