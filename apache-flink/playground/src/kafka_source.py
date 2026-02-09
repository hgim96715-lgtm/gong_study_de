import os
from pyflink.common import SimpleStringSchema,WatermarkStrategy
from pyflink.datastream import StreamExecutionEnvironment
from pyflink.datastream.connectors.kafka import KafkaSource,KafkaOffsetsInitializer

def run_kafka_source():
    # env설정 
    env=StreamExecutionEnvironment.get_execution_environment()
    
    jar_path="file:///opt/flink/lib/flink-sql-connector-kafka-3.1.0-1.18.jar"
    env.add_jars(jar_path)
    
    print(f"Loaded JAR from :{jar_path}")
    
    # Kafka Source설정
    source=(
        KafkaSource.builder()
        .set_bootstrap_servers("kafka:9092")
        .set_topics("input-topic")
        .set_group_id("my-flink-group")
        .set_starting_offsets(KafkaOffsetsInitializer.earliest())
        .set_value_only_deserializer(SimpleStringSchema())
        .build()
    )
    
    # DataStream 생성
    stream=env.from_source(source,WatermarkStrategy.no_watermarks(),"Kafka Source")
    
    # 데이터 출력
    stream.print()
    
    # 실행
    env.execute("PyFlink Kafka Source Job")
    
if __name__=="__main__":
    run_kafka_source()
    