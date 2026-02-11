"""
[PyFlink] Custom Trigger Example Job"
목표: 
  1. 데이터가 2개 모이면 즉시 발사 
  2. 2개가 안 모여도 20초(윈도우 종료)가 되면 무조건 발사 (Timeout)
입력: "Alice",1
출력: ("Alice",N)  N은 집계된 값
"""


import os
from pyflink.common import WatermarkStrategy, SimpleStringSchema
from pyflink.common.typeinfo import Types
from pyflink.datastream import StreamExecutionEnvironment
from pyflink.datastream.connectors.kafka import KafkaSource, KafkaSink, KafkaRecordSerializationSchema, KafkaOffsetsInitializer
from pyflink.datastream.window import TumblingProcessingTimeWindows, Trigger, TriggerResult
from pyflink.datastream.state import ValueStateDescriptor
from pyflink.common.time import Time

class CountTimeoutTrigger(Trigger):
    def __init__(self,max_count):
        self.max_count=max_count
        self.count_state_desc=ValueStateDescriptor("count",Types.INT())
        
    def on_element(self,element,timestamp,window,ctx):
      # 타이머 등록
      ctx.register_processing_time_timer(window.max_timestamp())
      # 상태 접근 
      count_state=ctx.get_partitioned_state(self.count_state_desc)
      
      # 내용확인 .value()
      current_count=count_state.value()
      
      # Null check
      # 처음엔 0이 아니라 None 초기화 필수
      if current_count is None:
          current_count=0
          
      current_count+=1
      count_state.update(current_count)
      
      # 목표 개수 도달 여부 확인
      if current_count >= self.max_count:
        # 개수 초기화
        count_state.clear()
        return TriggerResult.FIRE
      
      return TriggerResult.CONTINUE
    
    # 서버시간 (Processing Time) 타이머 발동시
    def on_processing_time(self,time,window,ctx):
      return TriggerResult.FIRE
    
    # 데이터 시간(Event Time/Watermark) 타이머 발동시
    def on_event_time(self,time,window,ctx):
      return TriggerResult.CONTINUE
    
    # 윈도우 종료시
    def clear(self,window,ctx):
      count_state=ctx.get_partitioned_state(self.count_state_desc)
      count_state.clear()
      
    # merge 필요시 구현
    def on_merge(self,window,ctx):
      pass
    

def run_custom_trigger():
  env=StreamExecutionEnvironment.get_execution_environment()
  jar_path = "file:///opt/flink/lib/flink-sql-connector-kafka-3.1.0-1.18.jar"
  env.add_jars(jar_path)
  
  source=(
    KafkaSource
    .builder()
    .set_bootstrap_servers("kafka:9092")
    .set_topics("input-topic")
    .set_group_id("custom-trigger-group")
    .set_starting_offsets(KafkaOffsetsInitializer.latest())
    .set_value_only_deserializer(SimpleStringSchema())
    .build()
  )
  
  stream=env.from_source(source,WatermarkStrategy.no_watermarks(),"Kafka Source")
  
  result_stream=(
    stream
    .map(lambda x: (x.split(",")[0],int(x.split(",")[1])) , output_type=Types.TUPLE([Types.STRING(),Types.INT()]))
    .key_by(lambda x: x[0])
    .window(TumblingProcessingTimeWindows.of(Time.seconds(20)))
    .trigger(CountTimeoutTrigger(max_count=2))
    .reduce(lambda a,b: (a[0],a[1]+b[1]))
  )
  
  result_stream.print()
  env.execute("Custom Trigger Example Job")

if __name__ == "__main__":
    run_custom_trigger()