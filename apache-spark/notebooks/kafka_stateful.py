from pyspark.sql import SparkSession
from pyspark.sql.types import  StructType, StructField, StringType, IntegerType
from pyspark.sql.functions import from_json, col,sum
spark=(
    SparkSession
    .builder
    .master("spark://spark-master:7077")
    .appName("kafkaStateful")
    .config("spark.streaming.stopGracefullyOnShutdown","true")
    .config("spark.sql.shuffle.partitions","3")
    .getOrCreate()
)

schema=StructType([
    StructField("product_id",StringType()),
    StructField("amount",IntegerType())
])

events=(
    spark
    .readStream
    .format("kafka")
    .option("kafka.bootstrap.servers","kafka:9092")
    .option("subscribe","pos")
    .option("startingOffsets","earliest")
    .option("failOnDataLoss","false")
    .load()
)

value_df=(
    events.select(
        col('key'),
        from_json(col("value").cast("string"),schema).alias("value"))
)

tf_df=value_df.selectExpr(
    'value.product_id',
    'value.amount'
)
total_df=(
    tf_df
    .groupBy("product_id")
    .agg(sum("amount").alias("total_amount"))
)
query=(
    total_df
    .writeStream
    .outputMode("complete")
    .format("console")
    .start()
)
query.awaitTermination()

