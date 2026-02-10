"""
[PyFlink] Kafka Reduce Operator Example
목표: ("Alice", 1) 형태의 문자열 데이터를 안전하게 파싱하여, 이름별 합계를 구한다.
핵심: ast.literal_eval을 사용한 안전한 튜플 변환 ⭐️
"""
import os
import ast
from pyflink.common import SimpleStringSchema, WatermarkStrategy
from pyflink.common.typeinfo import Types
from pyflink.datastream import StreamExecutionEnvironment
from pyflink.datastream.connectors.kafka import KafkaSource, KafkaSink, KafkaRecordSerializationSchema, KafkaOffsetsInitializer

def run_reduce():
    
    # 환경설정
    env=StreamExecutionEnvironment.get_execution_environment()

    
    # jar 파일 로딩
    jar_path="file:///opt/flink/lib/flink-sql-connector-kafka-3.1.0-1.18.jar"
    env.add_jars(jar_path)
    
    # Kafka Source 설정 
    source=(
        KafkaSource
        .builder()
        .set_bootstrap_servers("kafka:9092")
        .set_topics("input-topic")
        .set_group_id("operator-group")
        .set_starting_offsets(KafkaOffsetsInitializer.earliest())
        .set_value_only_deserializer(SimpleStringSchema())
        .build()
    )
    
    stream=env.from_source(source,WatermarkStrategy.no_watermarks(),"Kafka Source")
    
    # reduce 함수 활용
    mapped_stream=stream.map(
        lambda x:ast.literal_eval(x),
        output_type=Types.TUPLE([Types.STRING(), Types.INT()])
    )
    
    keyed_stream=mapped_stream.key_by(lambda x:x[0])
    
    reduced_stream=keyed_stream.reduce(
        lambda a,b : (a[0], a[1]+b[1])
    )
    
    # Kafka Sink 설정
    
    sink=(
        KafkaSink
        .builder()
        .set_bootstrap_servers("kafka:9092")
        .set_record_serializer(
            KafkaRecordSerializationSchema
            .builder()
            .set_topic("output-topic")
            .set_value_serialization_schema(SimpleStringSchema())
            .build()
        )
    ).build()
    
    # 결과를 문자열로 변환하여 Kafka로 출력
    result_stream=reduced_stream.map(
        lambda x: f"{x[0]}:{x[1]}",
        output_type=Types.STRING()
    )
    result_stream.sink_to(sink)
    
    env.execute("Kafka Reduce Operator Example")

if __name__=="__main__":
    run_reduce()