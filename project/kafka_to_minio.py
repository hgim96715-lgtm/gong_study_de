from kafka import KafkaConsumer
import pandas as pd
import json
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

MINIO_ENDPOINT=os.getenv('MINIO_ENDPOINT')
MINIO_ACCESS_KEY=os.getenv('MINIO_ACCESS_KEY')
MINIO_SECRET_KEY=os.getenv('MINIO_SECRET_KEY')
BUCKET_NAME=os.getenv('MINIO_BUCKET_NAME')

storage_options={
    'key':MINIO_ACCESS_KEY,
    'secret':MINIO_SECRET_KEY,
    'client_kwargs':{"endpoint_url":MINIO_ENDPOINT}
}

consumer=KafkaConsumer(
    'user-log',
    bootstrap_servers=['localhost:29092'],
    auto_offset_reset='latest',
    value_deserializer=lambda x:json.loads(x.decode('utf-8'))
)
print("Data Lake 실행중!!")
print(storage_options)

buffer=[]
BATCH_SIZE=10

for message in consumer:
    buffer.append(message.value)
    print(f"📦 바구니에 담는 중... ({len(buffer)}/{BATCH_SIZE})")
    
    if len(buffer)>=BATCH_SIZE:
        df=pd.DataFrame(buffer)
        now=datetime.now().strftime("%Y%m%d_%H%M%S")
        file_path=f"s3://{BUCKET_NAME}/{now}_raw.parquet"
        
        try:
            df.to_parquet(
                file_path,
                engine="pyarrow",
                compression="snappy",
                index=False,
                storage_options=storage_options
            )
            print(f"저장완료:{file_path}")
        except Exception as e:
            print(f"저장실패 {e}")
        finally:
            buffer.clear()