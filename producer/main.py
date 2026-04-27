from fastapi import FastAPI
from producer.models import Transaction
from producer.producer import generate_transaction
from messaging.kafka_producer import send_transaction

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