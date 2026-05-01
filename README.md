# Fraud Detection Streaming Pipeline

Real-time fraud detection system that processes banking transactions as they happen, identifying suspicious patterns and alerting in under a second.

Built as a portfolio project targeting Data Engineer roles in fintech and digital banking.

---

## Why this project

Card fraud costs the financial industry billions annually. Traditional batch processing detects fraud hours after it occurs — by then, the damage is done. This project implements a **streaming architecture** that processes each transaction the moment it arrives, applying fraud detection rules in real time.

---

## Architecture

```
FastAPI (Transaction Generator)
        ↓
Kafka (Message Bus — topic: transactions)
        ↓
Spark Structured Streaming (Fraud Detection Engine)
        ↓
Redis (Real-time Alert Storage)
        ↓
Streamlit (Live Dashboard)
```

All services run locally via Docker Compose with automatic startup ordering and health checks.

---

## Tech Stack

| Layer | Technology |
|---|---|
| Transaction Producer | Python, FastAPI, Pydantic |
| Message Bus | Apache Kafka |
| Stream Processing | Apache Spark Structured Streaming, PySpark |
| Alert Storage | Redis |
| Dashboard | Streamlit |
| Infrastructure | Docker, Docker Compose |
| Data Validation | Pydantic v2 |
| IaC (defined) | Terraform |

---

## Fraud Detection Logic

The system currently detects **velocity fraud** — a card making too many transactions in a short time window, a classic indicator of card cloning or account takeover.

**Rule:** More than 3 transactions from the same card within a 5-minute tumbling window triggers an alert.

Additional patterns defined (extensible):
- Unusual geographic patterns
- Amounts outside normal user behaviour

---

## Transaction Schema

Each transaction event contains:

```json
{
  "transaction_id": "uuid",
  "card_id": "CARD123456",
  "amount": 432.50,
  "currency": "EUR",
  "merchant_id": "MERCH1234",
  "transaction_type": "PURCHASE",
  "location": "Madrid",
  "timestamp": "2026-04-30T14:32:11"
}
```

---

## How to Run

**Requirements:** Docker Desktop with WSL2 integration enabled.

```bash
# Clone the repository
git clone https://github.com/ferborao/fraud-detection-streaming
cd fraud-detection-streaming

# Start all services
docker compose up --build
```

This will start Zookeeper, Kafka, FastAPI, Spark consumer, Redis and the Streamlit dashboard in the correct order automatically.

**Access:**
- Transaction API + docs: `http://localhost:8000/docs`
- Fraud dashboard: `http://localhost:8501`

---

## Demo

**Simulate realistic traffic:**

From `http://localhost:8000/docs`, call `/start-stream` — this sends 100 transactions with embedded fraud patterns (same card ID repeated every 5 transactions).

**Force immediate fraud alert:**

Call `/simulate-fraud/{card_id}` with any card ID — sends 5 transactions for that card instantly.

Watch `http://localhost:8501` update in real time as alerts are detected.

---

## Project Structure

```
fraud-detection-streaming/
├── producer/          # FastAPI transaction generator
├── messaging/         # Kafka producer client
├── consumer/          # Spark Structured Streaming fraud detector
├── dashboard/         # Streamlit real-time dashboard
├── terraform/         # Azure infrastructure as code (defined, not deployed)
├── docker-compose.yml
└── requirements.txt
```

---

## Author

Fernando Borao · [LinkedIn](https://linkedin.com/in/fernandoborao) · [GitHub](https://github.com/ferborao)