from pyspark.sql import SparkSession
from pyspark.sql.types import  StructType, StructField, StringType
from pyspark.sql.functions import expr, from_json, col, lower, to_json, struct


spark=(
    SparkSession
    .builder
    .appName("StructuredMulti")
    .master("spark://spark-master:7077")
    .config("spark.streaming.stopGracefullyOnShutdown", "true")
    .config("spark.sql.shuffle.partitions", "3")
    .getOrCreate()
)

schema = StructType([
            StructField("city", StringType()),
            StructField("domain", StringType()),
            StructField("event", StringType())
        ])

events=(
    spark
    .readStream
    .format("kafka")
    .option("subscribe","pra-json")
    .option("kafka.bootstrap.servers","kafka:9092")
    .option("startingOffsets","earliest")
    .load()
)

value_df=events.select(
    col('key'),
    from_json(
        col("value").cast("string"),schema).alias("value"))

tf_df=value_df.selectExpr(
    'value.city',
    'value.domain',
    'value.event as behavior'
)

concat_df=(
    tf_df
    .withColumn('lower_city',lower(col('city')))
    .withColumn('domain',expr('domain'))
    .withColumn('behavior',expr('behavior'))
    .drop('city')
)

output_df = concat_df.select(
    to_json(struct(col("lower_city"), col("domain"), col("behavior"))).alias("value")
)

file_writer = concat_df \
                .writeStream \
                .queryName("transformed json") \
                .format("json") \
                .outputMode("append") \
                .option("path", "data/transformed") \
                .option("checkpointLocation", "chk/json") \
                .start()

kafka_writer = output_df \
                .writeStream \
                .queryName("transformed kafka") \
                .format("kafka") \
                .option("kafka.bootstrap.servers", "kafka:9092") \
                .option("checkpointLocation", "chk/kafka") \
                .option("topic", "transformed") \
                .outputMode("append") \
                .start()


spark.streams.awaitAnyTermination()










