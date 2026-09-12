from pyspark.sql import SparkSession
from pyspark.sql.functions import col, from_json
from pyspark.sql.types import (
    StructType,
    StructField,
    StringType,
    MapType
)
from pymongo import MongoClient
from datetime import datetime, timezone

spark = (
    SparkSession.builder
    .appName("BEACON-Analytics")
    .master("local[*]")
    .config(
        "spark.jars.packages",
        ",".join([
            "org.apache.spark:spark-sql-kafka-0-10_2.13:4.2.0",
            "org.mongodb.spark:mongo-spark-connector_2.13:10.5.0"
        ])
    )
    .getOrCreate()
)

spark.sparkContext.setLogLevel("WARN")

kafka_df = (
    spark.readStream
    .format("kafka")
    .option("kafka.bootstrap.servers", "localhost:9092")
    .option("subscribe", "beacon-events")
    .option("startingOffsets", "latest")
    .load()
)

events = kafka_df.select(
    col("value").cast("string").alias("json")
)

schema = StructType([
    StructField("timestamp", StringType(), True),
    StructField("event_type", StringType(), True),
    StructField("data", MapType(StringType(), StringType()), True)
])

parsed = (
    events
    .select(from_json("json", schema).alias("event"))
    .select("event.*")
)

# feature engineering
def process_batch(batch_df, batch_id):
    if batch_df.isEmpty():
        return

    print()
    print("="*30)
    print(f"Processing analytics batch: {batch_id}")
    print("="*30)

    client = MongoClient(
        "mongodb://localhost:27017"
    )

    db = client["beacon"]

    processed_collection = db["processed_events"]
    features_collection = db["features"]
    pending_collection = db["pending_requests"]

    rows = (
        batch_df
        .orderBy("timestamp")
        .collect()
    )

    for row in rows:
        timestamp = row["timestamp"]
        event_type = row["event_type"]
        data = row["data"]

        processed_document = {
            "timestamp": timestamp,
            "event_type": event_type,
            "data": dict(data) if data else {}
        }

        processed_collection.insert_one(
            processed_document
        )

        if event_type == "LLM_REQUEST":
            conversation_id = data.get(
                "conversation_id"
            )

            if conversation_id:
                request_document = {
                    "conversation_id": conversation_id,
                    "request_timestamp": timestamp,
                    "created_at": datetime.now(timezone.utc)
                }

                # pending_collection.replace_one(
                #     {
                #         "conversation_id": conversation_id
                #     },
                #     request_document,
                #     upsert=True
                # )

                pending_collection.insert_one(
                    request_document
                )

                print(
                    f"[REQUEST] "
                    f"{conversation_id} "
                    f"@ {timestamp}"
                )

        elif event_type == "LLM_RESPONSE":
            conversation_id = data.get(
                "conversation_id"
            )
            if not conversation_id:
                continue

            request = pending_collection.find_one(
                {
                    "conversation_id": conversation_id
                },
                sort=[("request_timestamp", 1)]
            )

            if request is None:
                print(
                    f"[WARNING] No matching request "
                    f"for response in conversation "
                    f"{conversation_id}"
                )
                continue

            try:
                request_time = datetime.fromisoformat(
                    request["request_timestamp"]
                )
                response_time = datetime.fromisoformat(
                    timestamp
                )
            except Exception as e:
                print(
                    f"[ERROR] Timestamp parsing failed: "
                    f"{e}"
                )
                continue

            latency = (response_time - request_time).total_seconds()

            feature_document = {
                "conversation_id": conversation_id,
                "feature_type": "LLM_RESPONSE_LATENCY",
                "latency_seconds": latency,
                "request_timestamp": request["request_timestamp"],
                "response_timestamp": timestamp
            }

            features_collection.insert_one(
                feature_document
            )

            print(
                f"[FEATURE] "
                f"LLM_RESPONSE_LATENCY = "
                f"{latency:.3f} seconds"
            )

            pending_collection.delete_one(
                {
                    "_id": request["_id"]
                }
            )
    client.close()



query = (
    parsed.writeStream
    .foreachBatch(process_batch)
    .option(
        "checkpointLocation",
        "D:/spark-checkpoints/beacon_features"
    )
    .start()
)

query.awaitTermination()