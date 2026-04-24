FROM bitnamilegacy/spark:3.4.1


USER root
RUN apt-get update && apt-get install -y python3-pip

WORKDIR /app
COPY processing/requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

COPY processing/ .

ENV KAFKA_HOST=kafka:9092
ENV POSTGRES_HOST=postgres

CMD ["spark-submit", "--packages", "org.apache.spark:spark-sql-kafka-0-10_2.12:3.4.0,org.postgresql:postgresql:42.6.0", "spark_streaming.py"]
