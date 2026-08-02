from pyspark.sql import SparkSession
from pyspark.sql.functions import col
from pyspark.sql.types import (
    StructType,
    StructField,
    StringType,
    MapType
)
from pyspark.sql.functions import from_json

spark = (
    SparkSession.builder
    .appName("BEACON")
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

# schema = StructType([
#     StructField("timestamp", StringType()),
#     StructField("event_type", StringType()),
#     StructField(
#         "data",
#         MapType(StringType(), StringType())
#     )
# ])

# parsed = (
#     events
#     .select(from_json("json", schema).alias("event"))
#     .select("event.*")
# )

query = (
    events.writeStream
    .format("mongodb")
    .option(
        "connection.uri",
        "mongodb://localhost:27017"
    )
    .option(
        "database",
        "beacon"
    )
    .option(
        "collection",
        "events"
    )
    .outputMode("append")
    .option(
        "checkpointLocation",
        "D:/spark-checkpoints/beacon"
    )
    .start()
)

query.awaitTermination()
