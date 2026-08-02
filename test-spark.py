from pyspark.sql import SparkSession

spark = (
    SparkSession.builder
    .master("local[*]")
    .appName("Test")
    .getOrCreate()
)

df = spark.createDataFrame(
    [
        (1, "hello"),
        (2, "world")
    ],
    ["id", "text"]
)

df.show()

spark.stop()