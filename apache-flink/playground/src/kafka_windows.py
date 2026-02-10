"""
[PyFlink] Word Count Window Example
목표: Kafka에서 "hi" 같은 단어가 들어오면 30초 동안 모아서 카운트를 셉니다.
입력: "hi"
출력: "Window Result -> hi: 3"
"""

import os
from pyflink.common import SimpleStringSchema, WatermarkStrategy
from pyflink.common.typeinfo import Types
from pyflink.datastream import StreamExecutionEnvironment
from pyflink.datastream.connectors.kafka import KafkaSource, KafkaSink, KafkaRecordSerializationSchema, KafkaOffsetsInitializer
from pyflink.datastream.window import TumblingProcessingTimeWindows
# Sliding 윈도우 임포트 
# from pyflink.datastream.window import SlidingProcessingTimeWindows
from pyflink.common.time import Time

def run_window_wordCount():
    
    # 환경설정
    env=StreamExecutionEnvironment.get_execution_environment()
    jar_path = "file:///opt/flink/lib/flink-sql-connector-kafka-3.1.0-1.18.jar"
    env.add_jars(jar_path)
    
    
    # source 설정
    source=(
        KafkaSource
        .builder()
        .set_bootstrap_servers("kafka:9092")
        .set_topics("input-topic")
        .set_group_id("window-wordcount-group")
        .set_starting_offsets(KafkaOffsetsInitializer.latest())
        .set_value_only_deserializer(SimpleStringSchema())
        .build()
    )
    
    stream=env.from_source(source, WatermarkStrategy.no_watermarks(), "Kafka Source")
    
    
    # operator
    mapped_stream=stream.map(
        lambda x: (x,1),
        output_type=Types.TUPLE([Types.STRING(), Types.INT()])
    )
    
    #key_by + window+reduce
    windowed_stream=(
        mapped_stream
        .key_by(lambda x:x[0])
        .window(TumblingProcessingTimeWindows.of(Time.seconds(30)))
        # .window(SlidingProcessingTimeWindows.of(Time.seconds(30), Time.seconds(10)))
        .reduce(lambda a, b: (a[0], a[1] + b[1]))
    )
    
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
    
    windowed_stream.map(
        lambda x: f"window result 30 seconds ->{x[0]}: {x[1]}",
        output_type=Types.STRING()
    ).sink_to(sink)
    
    env.execute("Kafka Window WordCount")

if __name__ == "__main__":
    run_window_wordCount()
    
    
    