from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col
from pyspark.sql.types import StructType, StringType, DoubleType, LongType

spark = SparkSession.builder \
    .appName("ISSTracker") \
    .master("local[*]") \
    .getOrCreate()

schema = StructType() \
    .add("message", StringType()) \
    .add("timestamp", LongType()) \
    .add("iss_position", StructType()
         .add("latitude", StringType())
         .add("longitude", StringType()))

df = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "localhost:9092") \
    .option("subscribe", "iss-location") \
    .load()

json_df = df.selectExpr("CAST(value AS STRING) as json") \
    .select(from_json(col("json"), schema).alias("data")) \
    .select("data.*")

json_df.writeStream \
    .format("parquet") \
    .option("path", "data/iss_parquet") \
    .option("checkpointLocation", "data/checkpoint") \
    .outputMode("append") \
    .start() \
    .awaitTermination()
