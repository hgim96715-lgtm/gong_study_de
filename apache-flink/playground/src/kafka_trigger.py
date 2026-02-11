"""
[PyFlink] Trigger Example
윈도우는 10초 동안 유지되지만, 데이터가 2개 도착할 때마다 결과를 출력합니다.
`.trigger(CountTrigger)`를 설정하면 기본 시간 트리거(Default Time Trigger)가 비활성화 됩니다.
두개다 설정하려면 custom trigger를 구현해야 합니다.
"""


import os
import ast
from pyflink.common import WatermarkStrategy, SimpleStringSchema
from pyflink.common.typeinfo import Types
from pyflink.datastream import StreamExecutionEnvironment
from pyflink.datastream.connectors.kafka import KafkaSource, KafkaSink, KafkaRecordSerializationSchema, KafkaOffsetsInitializer
from pyflink.datastream.window import TumblingProcessingTimeWindows, CountTrigger 
from pyflink.common.time import Time

def run_trigger_example():
    
    env=StreamExecutionEnvironment.get_execution_environment()
    jar_path = "file:///opt/flink/lib/flink-sql-connector-kafka-3.1.0-1.18.jar"
    env.add_jars(jar_path)
    
    source=(
        KafkaSource
        .builder()
        .set_bootstrap_servers("kafka:9092")
        .set_topics("input-topic")
        .set_group_id("trigger-group")
        .set_starting_offsets(KafkaOffsetsInitializer.latest())
        .set_value_only_deserializer(SimpleStringSchema())
        .build()
    )
    
    stream=env.from_source(source,WatermarkStrategy.no_watermarks(), "Kafka Source")
    
    result_stream=(
        stream
        .map(lambda x:(x.split("-")[0],int(x.split("-")[1])),output_type=Types.TUPLE([Types.STRING(),Types.INT()]))
        .key_by(lambda x:x[0])
        .window(TumblingProcessingTimeWindows.of(Time.seconds(10)))
        .trigger(CountTrigger.of(2))
        .reduce(lambda a,b:(a[0],a[1]+b[1]))
    )
    
    result_stream.print()
    
    env.execute("Kafka Trigger Example")   
    
if __name__=="__main__":
    run_trigger_example()