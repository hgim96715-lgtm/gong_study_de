import time
import json
import random
import uuid
from pathlib import Path
from datetime import datetime
from kafka import KafkaProducer
from kafka.errors import NoBrokersAvailable
from faker import Faker

fake=Faker('ko_KR')

TOPIC_NAME='user-log'

def generate_user_data():
    status_list=['pending','approved','shipped','delivered','canceled']
    payment_list=['credit_card','check_card','bank_transfer','voucher']
    status_weights=[5,10,20,60,5]
    payment_weights=[50,30,15,5]
    
    category_list=["패션","전자","식품","생활","스포츠"]
    
    order_status=random.choices(status_list,weights=status_weights,k=1)[0]
    payment_type=random.choices(payment_list,weights=payment_weights,k=1)[0]
    
    
    price = round(random.uniform(5000, 500000), -2)
    quantity=random.randint(1,5)
    total_amount=price*quantity
    
    data={
        "event_id":str(uuid.uuid4()),
        "order_id":str(uuid.uuid4()),
        "customer_id":str(uuid.uuid4()),
        "product_id":str(uuid.uuid4()),
        
        "order_status":order_status,
        "payment_type":payment_type,
        "price":price,
        "quantity":quantity,
        "total_amount":total_amount,
        "category":random.choice(category_list),
        "product_name":f"{fake.word()} 상품",
        
        "timestamp":datetime.now().isoformat(),
        "customer_name":fake.name(),
        "customer_city":fake.city(),
        "customer_state":fake.administrative_unit()
        
    }
    return data

if __name__ == "__main__":
    print(f"[Start] sending {TOPIC_NAME} topic!")
    producer=None
    Path(".stop_signal").unlink(missing_ok=True)
    for i in range(10):
        try:
            print(f"Kafka랑 연결중.. ({i+1}/10)")
            producer=KafkaProducer(
                bootstrap_servers='localhost:29092',
                value_serializer=lambda v:json.dumps(v).encode('utf-8')
            )
            print("Kafka랑 연결되었다!")
            break
        except NoBrokersAvailable:
            print(f"연결실패..")
            time.sleep(3)
            
    else:
        raise RuntimeError("10번 시도후에도 kafka랑 연결 실패했어요 😣")
    
    print(f"이제 함수를 전송..topic name:{TOPIC_NAME}")
    
    try:
        while True:
            stop_file=Path(".stop_signal")
            if stop_file.exists():
                print("Dashboard에서 종료버튼 클릭! Producer를 멈춥니다.")
                stop_file.unlink()
                break
            
            log=generate_user_data()
            producer.send(TOPIC_NAME,value=log)
            print(f" 전송 중: {log['customer_name']}님이 {log['product_name']}을 구매함 (금액: {log['total_amount']})")
            time.sleep(1)
    except KeyboardInterrupt:
        print("Stop..!")
        producer.close()
    finally:
        producer.close()