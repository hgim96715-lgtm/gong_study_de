from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, StringType
from pyspark.sql.functions import expr, from_json, col, lower, to_json, struct

spark = SparkSession \
    .builder \
    .appName("StructuredJSONETL") \
    .config("spark.streaming.stopGracefullyOnShutdown", "true") \
    .config("spark.sql.shuffle.partitions", "3") \
    .getOrCreate()

# 스키마 정의 
schema = StructType([
            StructField("city", StringType()),
            StructField("domain", StringType()),
            StructField("event", StringType())
        ])

# 카프카 읽기 
# 입력 통신 topic은 pra-json
events = spark \
    .readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "kafka:9092") \
    .option("subscribe", "pra-json") \
    .option("startingOffsets", "earliest") \
    .option("failOnDataLoss", "false") \
    .load()

# kafka 데이터는 value라는 이름의 Binary(택배상자) 
#(Binary -> JSON 구조체)
value_df = events.select(
            col('key'),
            from_json(col("value").cast("string"), schema).alias("value"))

# seectExpr : sql처럼 꺼내 올수 있다 
tf_df = value_df.selectExpr(
            'value.city',
            'value.domain',
            'value.event as behavior')

# expr : 컬럼안에서 sql수식 가능하다
concat_df = tf_df.withColumn('lower_city', lower(col('city'))) \
                .withColumn('domain', expr('domain')) \
                .withColumn('behavior', expr('behavior')).drop('city')

# (Kafka로 보내기 위해)
# 컬럼  ->JSON 변환 to_json(struct(묶은데이터))
# struct 여러컬럼 하나로 묶기 
output_df = concat_df.select(
    to_json(struct(col("lower_city"), col("domain"), col("behavior"))).alias("value")
)

#  카프카로 전송 
# output 통신 transformed 
query = output_df \
    .writeStream \
    .queryName("transformed writer") \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "kafka:9092") \
    .option("checkpointLocation", "checkpoint") \
    .option("topic", "transformed") \
    .outputMode("append") \
    .start()

query.awaitTermination()