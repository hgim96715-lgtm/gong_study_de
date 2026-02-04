from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, StringType, IntegerType
from pyspark.sql.functions import from_json, col, to_timestamp, window, sum


spark = (
    SparkSession
    .builder
    .master("spark://spark-master:7077")  
    .appName("kafkaTumblingTime")              
    .config("spark.streaming.stopGracefullyOnShutdown", "true")
    .config("spark.sql.shuffle.partitions", "3") 
    .getOrCreate()
)


schema = StructType([
    StructField("create_date", StringType()),
    StructField("amount", IntegerType())
])


events = (
    spark
    .readStream
    .format("kafka")
    .option("kafka.bootstrap.servers", "kafka:9092")
    .option("subscribe", "timeseries") # 토픽 이름 확인       
    .option("startingOffsets", "earliest")
    .option("failOnDataLoss", "false")
    .load()
)


value_df = events.select(
    col('key'),
    from_json(col("value").cast("string"), schema).alias("value")
)

timestamp_format = "yyyy-MM-dd HH:mm:ss"

tf_df = (
    value_df
    .select("value.*")
    .withColumn("create_date", to_timestamp("create_date", timestamp_format))
)


window_duration = "5 minutes"

#withWatermart(이벤트시간컬럼,허용지연시간)
window_agg_df = (
    tf_df
    .withWatermark("create_date","10 minutes")
    .groupBy(window(col("create_date"), window_duration))                
    .agg(sum("amount").alias("total_amount"))
)


query = (
    window_agg_df
    .writeStream
    .outputMode("update")
    .format("console")
    .option("truncate", "false") 
    .trigger(processingTime="5 seconds")
    .start()
)

query.awaitTermination()