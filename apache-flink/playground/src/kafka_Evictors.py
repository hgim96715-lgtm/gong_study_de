"""
[PyFlink] kafka Evictors Example
입력 : "hello-3"
출력 예시: hello:3개 합계는 9입니다.
"""

import os
from pyflink.common import WatermarkStrategy, SimpleStringSchema
from pyflink.common.typeinfo import Types
from pyflink.datastream import StreamExecutionEnvironment
from pyflink.datastream.connectors.kafka import KafkaSource, KafkaOffsetsInitializer
from pyflink.datastream.window import TumblingProcessingTimeWindows
from pyflink.datastream.functions import ProcessWindowFunction 
from pyflink.common.time import Time



class KeepLastNFunction(ProcessWindowFunction):
    def __init__(self,n):
        self.n = n
    
    def process(self,key,context,elements):
        # elements interable 객체, 슬라이싱을 위해 list로 변환
        data_list=list(elements)
        
        evicted_list=data_list[-self.n:]
        
        total_sum=sum([item[1] for item in evicted_list])
        
        
        # yield(key,total_sum)
        result_msg=f"{key}:{self.n}개 합계는 {total_sum}입니다."
        yield result_msg


def run_evictor_example():
    env= StreamExecutionEnvironment.get_execution_environment()
    jar_path = "file:///opt/flink/lib/flink-sql-connector-kafka-3.1.0-1.18.jar"
    env.add_jars(jar_path)
    
    source=(
        KafkaSource
        .builder()
        .set_bootstrap_servers("kafka:9092")
        .set_topics("input-topic")
        .set_group_id("evictor-group")
        .set_starting_offsets(KafkaOffsetsInitializer.latest())
        .set_value_only_deserializer(SimpleStringSchema())
        .build()
    )
    
    stream=env.from_source(source, WatermarkStrategy.no_watermarks(), "Kafka Source")
    
    result_stream=(
        stream
        .map(lambda x:(x.split("-")[0],int(x.split("-")[1])), output_type=Types.TUPLE([Types.STRING(), Types.INT()]))
        .key_by(lambda x: x[0])
        .window(TumblingProcessingTimeWindows.of(Time.seconds(30)))
        .process(KeepLastNFunction(3))
    )
    result_stream.print()
    env.execute("Evictor Example")

if __name__ == "__main__":
    run_evictor_example()