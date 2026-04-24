from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col, window, avg, current_timestamp
from pyspark.sql.types import StructType, StructField, StringType, DoubleType, IntegerType, TimestampType

# Schema for the incoming Kafka events
schema = StructType([
    StructField("transaction_id", StringType(), True),
    StructField("user_id", StringType(), True),
    StructField("amount", DoubleType(), True),
    StructField("timestamp", StringType(), True),
    StructField("merchant_id", StringType(), True),
    StructField("location", StringType(), True),
    StructField("is_fraud", IntegerType(), True)
])

import os

def process_stream():
    kafka_host = os.getenv('KAFKA_HOST', 'kafka:9092')
    postgres_host = os.getenv('POSTGRES_HOST', 'postgres')
    
    spark = SparkSession.builder \
        .appName("FraudDetectionStreaming") \
        .config("spark.jars.packages", "org.apache.spark:spark-sql-kafka-0-10_2.12:3.4.0") \
        .getOrCreate()

    # 1. Read from Kafka
    df = spark.readStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", kafka_host) \
        .option("subscribe", "transactions") \
        .load()


    # 2. Parse JSON and add event time
    parsed_df = df.selectExpr("CAST(value AS STRING)") \
        .select(from_json(col("value"), schema).alias("data")) \
        .select("data.*") \
        .withColumn("event_time", col("timestamp").cast(TimestampType()))

    # 3. Feature Engineering: Windowed Aggregates
    # Calculate avg amount per user in a 10-minute sliding window
    windowed_features = parsed_df \
        .withWatermark("event_time", "10 minutes") \
        .groupBy(
            window(col("event_time"), "10 minutes", "5 minutes"),
            col("user_id")
        ).agg(avg("amount").alias("avg_amount_10m"))

    # 4. Sink to PostgreSQL (Warehouse)
    # In production, we use .writeStream.foreachBatch for multiple sinks
    def write_to_sinks(batch_df, batch_id):
        # Write to Postgres
        batch_df.write \
            .format("jdbc") \
            .option("url", f"jdbc:postgresql://{postgres_host}:5432/warehouse") \
            .option("dbtable", "transactions_processed") \
 \
            .option("user", "admin") \
            .option("password", "password") \
            .mode("append") \
            .save()
        
        # Write to Redis (Feature Store) - Pseudo-code for Redis Sink
        # batch_df.foreach(lambda row: redis_client.set(f"user:{row.user_id}:avg", row.avg_amount_10m))
        print(f"Batch {batch_id} processed and saved to DWH/FS.")

    query = parsed_df.writeStream \
        .foreachBatch(write_to_sinks) \
        .start()

    query.awaitTermination()

if __name__ == "__main__":
    process_stream()
