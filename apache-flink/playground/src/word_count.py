import os
import sys

from pyflink.common import Types, WatermarkStrategy
from pyflink.common.serialization import Encoder
from pyflink.datastream import StreamExecutionEnvironment
from pyflink.datastream.connectors import FileSource, StreamFormat, FileSink 

def word_count():
    env = StreamExecutionEnvironment.get_execution_environment()
    env.set_parallelism(1)
    
    input_path = 'file:///opt/flink/playground/data/input.txt'
    
    
    # 포맷이랑 경로를 지정해서 FileSource 생성
    source=FileSource.for_record_stream_format(
        StreamFormat.text_line_format(),
        input_path
    ).build()
    
    print(f"FileSource 객체구나! {source}")
    
    # FileSource를 environment에 등록
    ds=env.from_source(
        source=source,
        watermark_strategy=WatermarkStrategy.no_watermarks(),
        source_name='word_count_practice'
    )
    def split(line):
        for word in line.split():
            yield word
            
    # Tuple일 경우 , []대괄호를 사용 해서 타입 지정
    # key_by는 GroupBy 역할
    ds=(
        ds
        .flat_map(split,output_type=Types.STRING())
        .map(lambda i:(i,1),output_type=Types.TUPLE([Types.STRING(),Types.INT()]))
        .key_by(lambda x:x[0])
        .sum(1)
    )
    output_path = '/opt/flink/playground/data/output'
    # 파일로 저장하기
    sink=FileSink.for_row_format(
        base_path=output_path,
        encoder=Encoder.simple_string_encoder("UTF-8")
    ).build()
    
    
    ds.map(lambda i: f"{i[0]},{i[1]}", output_type=Types.STRING()).sink_to(sink)
    
    env.execute("word_count_20260206")
    
if __name__ == '__main__':
    word_count()