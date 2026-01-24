import sys
from pyspark.sql import SparkSession

def word_count(input_path: str, output_path: str):
    # [우리 방식] 설정은 spark-defaults.conf가 다 알아서 함!
    # 그냥 "스파크 줘!" 하면 끝.
    spark = SparkSession.builder.appName("WordCount").getOrCreate()

    # 1. 읽기 (s3a 경로를 그대로 읽음)
    text_file = spark.read.text(input_path)

    # 2. 계산 (Word Count 로직)
    # RDD 변환 -> 쪼개기(flatMap) -> (단어, 1) 만들기(map) -> 더하기(reduce)
    counts = (
        text_file.rdd.flatMap(lambda line: line[0].split())
        .map(lambda word: (word, 1))
        .reduceByKey(lambda a, b: a + b)
    )

    # 3. 저장
    print(f"Saving result to: {output_path}")
    counts.toDF(["word", "count"]) \
        .write \
        .mode("overwrite") \
        .csv(output_path, header=True)
    
    spark.stop()

if __name__ == "__main__":
    # 터미널에서 인자 2개를 받아서 실행
    if len(sys.argv) != 3:
        print("Usage: word_count.py <input_path> <output_path>")
        sys.exit(-1)
        
    word_count(sys.argv[1], sys.argv[2])