import os
from pyflink.common import SimpleStringSchema, WatermarkStrategy, SerializationSchema
from pyflink.datastream import StreamExecutionEnvironment
from pyflink.datastream.connectors.kafka import KafkaSource, KafkaSink, KafkaRecordSerializationSchema, KafkaOffsetsInitializer
from pyflink.common.typeinfo import Types

def run_kafka_sink():
    # env 설정 
    env=StreamExecutionEnvironment.get_execution_environment()
    
    # Jar파일 로딩
    jar_path="file:///opt/flink/lib/flink-sql-connector-kafka-3.1.0-1.18.jar"
    env.add_jars(jar_path)
    
    # Source 설정
    
    source=(
        KafkaSource
        .builder()
        .set_bootstrap_servers("kafka:9092")
        .set_topics("input-topic")
        .set_group_id("sink-group")
        .set_starting_offsets(KafkaOffsetsInitializer.earliest())
        .set_value_only_deserializer(SimpleStringSchema())
        .build()
    )
    
    stream=env.from_source(source, WatermarkStrategy.no_watermarks(), "Kafka Source")
    
    
    # 가공 설정
    processed_stream=stream.map(lambda x:f"Processed: {x.title()}", output_type=Types.STRING())
    
    
    # sink 설정
    sink=(
        KafkaSink
        .builder()
        .set_bootstrap_servers("kafka:9092")
        .set_record_serializer(
            KafkaRecordSerializationSchema
            .builder()
            .set_topic("output-topic") # 출력 토픽 설정
            .set_value_serialization_schema(SimpleStringSchema())
            .build()
        )
    ).build()

    # sink 호출
    
    processed_stream.sink_to(sink)
    
    env.execute("Flink Kafka Sink Job")
    
if __name__=="__main__":
    run_kafka_sink()