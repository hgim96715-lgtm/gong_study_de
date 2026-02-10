"""
[PyFlink] Window Average Example (AggregateFunction)
목표: Kafka 데이터를 10초간 모아서 '평균 값'을 계산한다.
입력: "Alice", 100, "Alice", 200
출력: "Window Result -> 150.0"
"""

import os
import ast
from pyflink.common import SimpleStringSchema, WatermarkStrategy
from pyflink.common.typeinfo import Types
from pyflink.datastream import StreamExecutionEnvironment
from pyflink.datastream.connectors.kafka import KafkaSource, KafkaSink, KafkaRecordSerializationSchema, KafkaOffsetsInitializer
from pyflink.datastream.window import TumblingProcessingTimeWindows
from pyflink.common.time import Time
from pyflink.datastream.functions import AggregateFunction

class AverageAggregate(AggregateFunction):
    
    # (총점, 개수)를 누적하는 accumulator 생성
    def create_accumulator(self):
        return (0,0) # (sum, count)
    
    # 더하기 
    # value: ("Alice", 100) -> value[1] = 100
    # accumulator: (current_sum, current_count)
    def add(self,value,accumulator):
        return (accumulator[0]+value[1],accumulator[1]+1)
    
    # 최종결과 계산
    def get_result(self,accumulator):
        return accumulator[0]/accumulator[1] if accumulator[1]>0 else 0.0
    
    # 병합 
    def merge(self,a,b):
        return (a[0]+b[0], a[1]+b[1])
    
def run_window_average():
    
    env=StreamExecutionEnvironment.get_execution_environment()
    jar_path = "file:///opt/flink/lib/flink-sql-connector-kafka-3.1.0-1.18.jar"
    env.add_jars(jar_path)
    
    source=(
        KafkaSource
        .builder()
        .set_bootstrap_servers("kafka:9092")
        .set_topics("input-topic")
        .set_group_id("avg-group")
        .set_starting_offsets(KafkaOffsetsInitializer.latest())
        .set_value_only_deserializer(SimpleStringSchema())
        .build()
    )
    
    stream=env.from_source(source,WatermarkStrategy.no_watermarks(), "Kafka Source")
    
    mapped_stream=stream.map(
        lambda x: (x.split(",")[0],int(x.split(",")[1])),
        output_type=Types.TUPLE([Types.STRING(),Types.INT()])
    )
    avg_stream=(
        mapped_stream
        .key_by(lambda x:x[0])
        .window(TumblingProcessingTimeWindows.of(Time.seconds(30)))
        .aggregate(
            AverageAggregate(),
            accumulator_type=Types.TUPLE([Types.INT(),Types.INT()]),
            output_type=Types.DOUBLE()
        )
    )
    
    sink=(
        KafkaSink
        .builder()
        .set_bootstrap_servers("kafka:9092")
        .set_record_serializer(
            KafkaRecordSerializationSchema.builder()
            .set_topic("output-topic")
            .set_value_serialization_schema(SimpleStringSchema())
            .build()
        )
    ).build()
    
    avg_stream.map(
        lambda x: f"window Result -> {x}",
        output_type=Types.STRING()
    ).sink_to(sink)
    
    env.execute("Kafka Window Average Example")
    

if __name__=="__main__":
    run_window_average()