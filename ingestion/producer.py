import json
import time
import random
from datetime import datetime
from kafka import KafkaProducer

import os

def get_producer():
    kafka_host = os.getenv('KAFKA_HOST', 'kafka:9092')
    return KafkaProducer(
        bootstrap_servers=[kafka_host],
        value_serializer=lambda v: json.dumps(v).encode('utf-8')
    )


def generate_transaction():
    """Generates a synthetic transaction."""
    user_id = f"user_{random.randint(1, 1000)}"
    amount = round(random.uniform(10, 5000), 2)
    
    # Simple fraud logic for simulation: very high amounts or specific users
    is_fraud = 1 if amount > 4500 or random.random() < 0.01 else 0
    
    return {
        "transaction_id": f"tx_{int(time.time() * 1000)}",
        "user_id": user_id,
        "amount": amount,
        "timestamp": datetime.now().isoformat(),
        "merchant_id": f"merchant_{random.randint(1, 50)}",
        "location": random.choice(["NY", "LON", "PAR", "TOK", "MUM"]),
        "is_fraud": is_fraud
    }

def run_producer():
    producer = get_producer()
    print("🚀 Kafka Producer started. Sending transactions...")
    try:
        while True:
            tx = generate_transaction()
            producer.send('transactions', tx)
            print(f"Sent: {tx['transaction_id']} | Amount: {tx['amount']} | Fraud: {tx['is_fraud']}")
            time.sleep(random.uniform(0.1, 1.0)) # Simulate varying traffic
    except KeyboardInterrupt:
        print("Stopping producer...")
    finally:
        producer.close()

if __name__ == "__main__":
    run_producer()
