import logging
import time
import sys
from kafka import KafkaConsumer
from kafka.errors import NoBrokersAvailable


logging.basicConfig(
    level=logging.INFO,
    stream=sys.stdout,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

for _ in range(10):
    try:
        consumer=KafkaConsumer(
            'iot-average-topic',
            bootstrap_servers='kafka:9092',
            auto_offset_reset='latest',
            enable_auto_commit=True,
            group_id='iot-consumer-group',
            value_deserializer=lambda x: x.decode('utf-8')
        )
        break
    except NoBrokersAvailable:
        print("Kafka는 아직 준비가 안됨, 재시도중...")
        time.sleep(3)
else:
    raise RuntimeError("Kafka broker를 재시도 후에도 사용할 수 없음")

print("Listening for messages on 'iot-average-topic'...")   


for message in consumer:
    logging.info(f"Received: {message.value}")
