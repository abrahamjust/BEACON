from pyspark.sql import SparkSession

spark = (
    SparkSession.builder
    .master("local[*]")
    .appName("RateTest")
    .getOrCreate()
)

rate = (
    spark.readStream
    .format("rate")
    .load()
)

query = (
    rate.writeStream
    .format("console")
    .outputMode("append")
    .start()
)

query.awaitTermination()