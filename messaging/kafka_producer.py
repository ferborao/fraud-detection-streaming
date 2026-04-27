import os
from dotenv import load_dotenv
from kafka import KafkaProducer
from producer.models import Transaction

load_dotenv()

# Configuración de Kafka
# KAFKA_BOOTSTRAP_SERVERS: dirección del broker
# KAFKA_TOPIC_TRANSACTIONS: nombre del topic donde se publican las transacciones
KAFKA_BOOTSTRAP_SERVERS = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "localhost:9092")
KAFKA_TOPIC_TRANSACTIONS = os.getenv("KAFKA_TOPIC_TRANSACTIONS", "transactions")

# Productor de Kafka usando la librería kafka-python
# - value_serializer: convierte el mensaje a bytes antes de enviar
# - key_serializer: serializa la clave del mensaje
producer = KafkaProducer(
    bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
    value_serializer=lambda v: v.encode("utf-8"),
    key_serializer=lambda k: k.encode("utf-8") if k else None,
)


def send_transaction(transaction: Transaction) -> None:
    """
    Serializa y envía una transacción al topic de Kafka.

    Proceso:
        1. Convierte el modelo Pydantic a JSON string -> model_dump_json()
        2. Envía al topic configurado -> producer.send()
        3. Asegura que se envíe inmediatamente -> producer.flush()
    """

    message = transaction.model_dump_json()
    producer.send(KAFKA_TOPIC_TRANSACTIONS, key=transaction.transaction_id, value=message)
    producer.flush()