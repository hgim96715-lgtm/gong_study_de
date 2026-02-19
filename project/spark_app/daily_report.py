from pyspark.sql import SparkSession
from pyspark.sql.functions import col,sum,count,desc,current_date
from dotenv import load_dotenv
import os

load_dotenv()


def daily_report():
    spark=(
        SparkSession
        .builder
        .appName("DailyReport")
        .getOrCreate()
    )
    print(">>> Spark: PostgreSQL 연결시도중..")
    
    jdbc_url="jdbc:postgresql://postgres:5432/airflow"
    db_properties={
        "user":os.getenv("DB_USER"),
        "password":os.getenv("DB_PASSWORD"),
        "driver":"org.postgresql.Driver"
    }
    
    try:
        df=spark.read.jdbc(url=jdbc_url,table="user_logs",properties=db_properties)
        today_df = df.filter(col("timestamp").cast("date") == current_date())
        
        print(f">>>데이터 로드 성공! (총 {df.count()}건)")
        
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
            table="report_category_sales",
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