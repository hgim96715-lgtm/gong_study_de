import logging
import sys
import time
import json
import random
from kafka import KafkaProducer
from kafka.errors import NoBrokersAvailable

# 로깅설정
logging.basicConfig(
    level=logging.INFO,
    stream=sys.stdout,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# kafka 연결
for _ in range(10):
    try:
        producer=KafkaProducer(
            bootstrap_servers='kafka:9092',
            value_serializer=lambda v:json.dumps(v).encode('utf-8')
        )
        break
    except NoBrokersAvailable:
        print("Kafka는 아직 준비가 안됨, 재시도중...")
        time.sleep(3)
else:
    raise RuntimeError("Kafka broker를 재시도 후에도 사용할 수 없음")

topic='iot-topic'
print(f"Producing gender-age messages to topic: {topic}")

# IoT 데이터 생성 및 전송
# ca : California, ny : New York, az : Arizona
# 지역별  3개 테스트 
states = ["ca", "ny", "az"]

topic='iot-topic'

for i in range(1000):
    state=random.choice(states)
    temperature=round(random.uniform(10.0,40.0),1) 
    message={
        'state':state,
        'temperature':temperature
    }
    producer.send(topic,value=message)
    logging.info(f"Sent: {message}")
    time.sleep(1)
    
producer.flush()
