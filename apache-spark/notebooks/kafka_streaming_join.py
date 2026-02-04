"""
두 개의 실시간 데이터 스트림( 클릭)을 `uuid`를 기준으로 조인하여, "누가 광고를 보고 실제로 클릭했는지"를 찾아내는 실습입니다

#impression
{"placement_id": "100", "uuid": "xyz-1234", "create_date": "2023-09-01 00:04:00", "campaign": "1001"}

# click
{"placement_id": "100", "uuid": "xyz-1234", "create_date": "2023-09-01 00:05:00"}


"""

from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, StringType
from pyspark.sql.functions import from_json, col, to_timestamp,sum

spark = (
    SparkSession
    .builder
    .master("spark://spark-master:7077")  
    .appName("StreamingJoin")              
    .config("spark.streaming.stopGracefullyOnShutdown", "true")
    .config("spark.sql.shuffle.partitions", "3") 
    .getOrCreate()
)

impression_schema= StructType([
    StructField("placement_id", StringType()),
    StructField("uuid", StringType()),
    StructField("create_date",StringType()),
    StructField("campaign",StringType())
])

click_schema=StructType([
    StructField("placement_id",StringType()),
    StructField("uuid",StringType()),
    StructField("create_date",StringType())
])

# impression_events=(
#     spark
#     .readStream
#     .format("kafka")
#     .option("kafka.bootstrap.servers", "kafka:9092")
#     .option("subscribe", "impression")
#     .option("startingOffsets", "earliest")
#     .option("failOnDataLoss", "false")
#     .load()
# )

# click_events=(
#     spark
#     .readStream
#     .format("kafka")
#     .option("kafka.bootstrap.servers", "kafka:9092")
#     .option("subscribe", "click")
#     .option("startingOffsets", "earliest")
#     .option("failOnDataLoss", "false")
#     .load()
# )

def read_kafka(spark,topic_name):
    return(
     spark
    .readStream
    .format("kafka")
    .option("kafka.bootstrap.servers", "kafka:9092")
    .option("subscribe", topic_name)
    .option("startingOffsets", "earliest")
    .option("failOnDataLoss", "false")
    .load()
    )

timestamp_format = "yyyy-MM-dd HH:mm:ss"

# imprdssions_df, clicks_df 로직이 같으므로 합치기
def parse_stream(df,schema,watermark_duration):
    return(
        df.select(from_json(col("value").cast("string"),schema).alias("value"))
        .select("value.*")
        .withColumn("create_date",to_timestamp("create_date",timestamp_format))
        .withWatermark("create_date",watermark_duration)
    )
impressions_df = parse_stream(read_kafka(spark, "impression"), impression_schema, "30 minutes")
clicks_df      = parse_stream(read_kafka(spark, "click"),      click_schema,      "10 minutes")

join_df=impressions_df.join(
    clicks_df,
    on=['uuid'],how="inner"
).drop(clicks_df.placement_id)

query=(
    join_df
    .writeStream
    .outputMode("append")
    .format("console")
    .start()
)

query.awaitTermination()

