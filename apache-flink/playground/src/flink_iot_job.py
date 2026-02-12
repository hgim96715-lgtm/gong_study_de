import logging
import sys
import json
import time

from pyflink.common import Types, SimpleStringSchema, WatermarkStrategy
from pyflink.datastream.state import ValueStateDescriptor
from pyflink.datastream import StreamExecutionEnvironment
from pyflink.datastream.functions import KeyedProcessFunction, RuntimeContext
from pyflink.datastream.connectors.kafka import KafkaSource, KafkaSink, KafkaRecordSerializationSchema, KafkaOffsetsInitializer


logging.basicConfig(
    level=logging.INFO,
    stream=sys.stdout,
    format="%(message)s"
)

class AverageProcessFunction(KeyedProcessFunction):
    def __init__(self):
        self.sum_state=None
        self.count_state=None
        self.timer_state=None
        
    def open(self, runtime_context: RuntimeContext):
        
        self.sum_state=runtime_context.get_state(
            ValueStateDescriptor("sum", Types.FLOAT())
        )
        self.count_state=runtime_context.get_state(
            ValueStateDescriptor("count", Types.LONG())
        )
        self.timer_state=runtime_context.get_state(
            ValueStateDescriptor("timer", Types.LONG())
        )
     
     # 타이머 설정 및 상태 업데이트   
    def process_element(self,value,ctx:KeyedProcessFunction.Context):
        current_temp=value[1]
        
        current_sum=self.sum_state.value()
        current_count=self.count_state.value()
        
        if current_sum is None:
            current_sum=0.0
        if current_count is None:
            current_count=0
            
        current_sum+=current_temp
        current_count+=1
        
        self.sum_state.update(current_sum)
        self.count_state.update(current_count)
        
        current_timer=self.timer_state.value()
        
        if current_timer is None:
            timer_time=ctx.timer_service().current_processing_time()+10000
            ctx.timer_service().register_processing_time_timer(timer_time)
            self.timer_state.update(timer_time)
    
    # 타이머가 발동되면 평균 계산 및 출력
    def on_timer(self,timestamp: int,ctx: KeyedProcessFunction.OnTimerContext):
        current_sum=self.sum_state.value()
        current_count=self.count_state.value()
        
        # 데이터가 있을 때만 평균 계산
        if current_count is not None and current_count >0:
            avg_temp=current_sum / current_count
            state_key=ctx.get_current_key()
            
            result_msg=f"State:{state_key}, 10초 평균 온도 :{avg_temp:.2f}°C"
            yield result_msg
            
            print(f"출력!:{result_msg}")
            
        # 상태 초기화
        self.sum_state.clear()
        self.count_state.clear()
        self.timer_state.clear()
        
def run_job():
    env=StreamExecutionEnvironment.get_execution_environment()
    env.set_parallelism(1)
    
    jar_path = "file:///opt/flink/lib/flink-sql-connector-kafka-3.1.0-1.18.jar"
    env.add_jars(jar_path)
    
    source=(
        KafkaSource
        .builder()
        .set_bootstrap_servers("kafka:9092")
        .set_topics("iot-topic")
        .set_group_id("flink-iot-group")
        .set_starting_offsets(KafkaOffsetsInitializer.latest())
        .set_value_only_deserializer(SimpleStringSchema())
        .build()
    )
    
    stream=env.from_source(source,WatermarkStrategy.no_watermarks(),"Kafka Source")
    
    processed_stream=(
        stream
        # 문자열 -> 파이썬 객체 변환
        .map(lambda x:json.loads(x),output_type=Types.PICKLED_BYTE_ARRAY())
        # 파이썬 객체 -> (state, temperature) 튜플 변환
        .map(lambda obj:(obj['state'],float(obj['temperature'])),output_type=Types.TUPLE([Types.STRING(),Types.FLOAT()]))
        # 상태별로 키 분할
        .key_by(lambda x:x[0])
        .process(AverageProcessFunction(),output_type=Types.STRING())
        
    )
    
    sink=(
        KafkaSink
        .builder()
        .set_bootstrap_servers("kafka:9092")
        .set_record_serializer(
            KafkaRecordSerializationSchema
            .builder()
            .set_topic("iot-average-topic")
            .set_value_serialization_schema(SimpleStringSchema())
            .build()
        )
    ).build()
    
    processed_stream.sink_to(sink)
    
    print("Flink IoT Job started...")
    env.execute("PyFlink IoT Job")
    
if __name__=="__main__":
    run_job()