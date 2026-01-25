import sys
from pyspark.sql import SparkSession

# 👇 여기에 Airflow 관련 코드는 한 줄도 없어야 합니다!
if __name__ == "__main__":
    spark = SparkSession.builder.appName("WordCountApp").getOrCreate()

    # 인자 확인
    if len(sys.argv) < 3:
        sys.exit("Usage: word_count_app.py <input> <output>")

    input_path = sys.argv[1]
    output_path = sys.argv[2]

    print(f"DEBUG: Reading {input_path} -> Writing to {output_path}")

    try:
        # 읽기
        df = spark.read.text(input_path)
        # 로직 (단어 세기)
        counts = df.rdd.flatMap(lambda x: x.value.split(" ")) \
                       .map(lambda x: (x, 1)) \
                       .reduceByKey(lambda a, b: a + b)
        # 쓰기
        counts.saveAsTextFile(output_path)
        print("DEBUG: Success!")
    except Exception as e:
        print(f"DEBUG: Error: {e}")
        raise e
    finally:
        spark.stop()