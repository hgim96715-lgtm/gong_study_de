"""
outer : 매칭되지 않은 데이터는 바로 나오지 않는다.
메모리를 많이 잡아먹기때문에, Watermark는 필수이고, 시간제약도 필수이다.

#impression
{"placement_id": "100", "uuid": "xyz-1234", "create_date": "2023-09-01 00:04:00", "campaign": "1001"}

# click
{"placement_id": "100", "uuid": "xyz-1234", "create_date": "2023-09-01 00:05:00"}


"""

from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, StringType
from pyspark.sql.functions import from_json, col, to_timestamp,sum,expr

spark = (
    SparkSession
    .builder
    .master("spark://spark-master:7077")  
    .appName("StreamingLeftOuterJoin")              
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
def parse_stream(df,schema,watermark_duration,prefix):
    return(
        df
        .select(from_json(col("value").cast("string"),schema).alias("value"))
        .select("value.*")
        .withColumn("create_date",to_timestamp("create_date",timestamp_format))
        .withColumnRenamed("create_date",f"{prefix}_date")
        .withColumnRenamed("uuid",f"{prefix}_uuid")
        .withWatermark(f"{prefix}_date",watermark_duration)
    )
impressions_df = parse_stream(read_kafka(spark, "impression"), impression_schema, "5 minutes","impr")
clicks_df      = parse_stream(read_kafka(spark, "click"),      click_schema,      "5 minutes","click")

join_df=impressions_df.join(
    clicks_df,
    expr(
        """
        impr_uuid=click_uuid AND
        click_date>=impr_date AND
        click_date<=impr_date + interval 5 minutes 
        """),"leftOuter").drop("click_uuid").drop(clicks_df.placement_id)

query=(
    join_df
    .writeStream
    .outputMode("append")
    .format("console")
    .start()
)

query.awaitTermination()

