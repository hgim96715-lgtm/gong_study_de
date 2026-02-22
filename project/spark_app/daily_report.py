from pyspark.sql import SparkSession
from pyspark.sql.functions import col,sum,count,desc,current_date
from dotenv import load_dotenv
import os

load_dotenv()


def daily_report():
    # spark=(
    #     SparkSession
    #     .builder
    #     .appName("DailyReport")
    #     .getOrCreate()
    # )
    # print(">>> Spark: PostgreSQL 연결시도중..")
    # MINIO
    spark = (
        SparkSession
        .builder
        .appName("MinIO_DataLake_Report")
        # S3A 인증 설정
        .config("spark.hadoop.fs.s3a.endpoint", os.getenv("MINIO_ENDPOINT"))
        .config("spark.hadoop.fs.s3a.access.key", os.getenv("MINIO_ACCESS_KEY"))
        .config("spark.hadoop.fs.s3a.secret.key", os.getenv("MINIO_SECRET_KEY"))
        # S3A 동작 설정
        .config("spark.hadoop.fs.s3a.path.style.access", "true")
        .config("spark.hadoop.fs.s3a.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem")
        .config("spark.hadoop.fs.s3a.aws.credentials.provider", "org.apache.hadoop.fs.s3a.SimpleAWSCredentialsProvider")
        .config("spark.hadoop.fs.s3a.connection.ssl.enabled", "false")
        # ✅ 타임아웃 설정 (hang 방지)
        .config("spark.hadoop.fs.s3a.connection.timeout", "10000")
        .config("spark.hadoop.fs.s3a.connection.establish.timeout", "5000")
        .config("spark.hadoop.fs.s3a.attempts.maximum", "3")
        # ✅ MinIO 호환성 설정
        .config("spark.hadoop.fs.s3a.multipart.size", "104857600")
        .config("spark.hadoop.fs.s3a.fast.upload", "true")
        .getOrCreate()
    )
    print(">>> Spark : MINIO연결")
    

    
    jdbc_url="jdbc:postgresql://postgres:5432/airflow"
    db_properties={
        "user":os.getenv("DB_USER"),
        "password":os.getenv("DB_PASSWORD"),
        "driver":"org.postgresql.Driver"
    }
    
    try:
        # df=spark.read.jdbc(url=jdbc_url,table="user_logs",properties=db_properties)
        
        print(">>>MINIO에서 파일 수집")
        df = spark.read.parquet("s3a://raw-data/")
        today_df = df.filter(col("timestamp").cast("date") == current_date())
        
        print(f">>>데이터 로드 성공! (총 {df.count()}건)")
        df.show(5)
        
        report_df=(
            today_df
            .groupBy("category")
            .agg(
                count("order_id").alias("total_orders"),
                sum("total_amount").alias("total_sales")
            )
            .orderBy(col("total_sales").desc())
        )
        
        print("\n 오늘의 카테고리별 매출 Report")
        report_df.show()
        
        
        # 결과를 DB에 저장
        print(">>>DB에 Report저장중")
        report_df.write.jdbc(
            url=jdbc_url,
            # table="report_category_sales",
            table='report_category_sales_minio',
            mode="overwrite",
            properties=db_properties
        )
        print(">>>저장완료!!!")
        
    
    except Exception as e:
        print(f"\n Error ! {e}")
        raise e
        
    finally:
        spark.stop()
    
if __name__=="__main__":
    daily_report()