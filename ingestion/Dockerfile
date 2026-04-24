FROM python:3.9-slim

WORKDIR /app

COPY ingestion/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY ingestion/ .

ENV KAFKA_HOST=kafka:9092

CMD ["python", "producer.py"]
