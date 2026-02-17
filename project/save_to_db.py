from kafka import KafkaConsumer
import json
import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

DB_CONFIG={
    "host":os.getenv("DB_HOST"),
    "port":os.getenv("DB_PORT"),
    "database":os.getenv("DB_NAME"),
    "user":os.getenv("DB_USER"),
    "password":os.getenv("DB_PASSWORD")
}

consumer=KafkaConsumer(
    'user-log',
    bootstrap_servers=['localhost:29092'],
    auto_offset_reset='latest',
    value_deserializer=lambda x:json.loads(x.decode('utf-8'))
)

def insert_data(conn,cur,data):
    sql="""
        INSERT INTO user_logs(
            event_id,order_id,customer_id,product_id,
            order_status,payment_type,price,quantity,total_amount,
            category,product_name,
            timestamp,
            customer_name,customer_city,customer_state
        )
        VALUES(
            %s, %s, %s, %s,
            %s,%s,%s,%s,%s,
            %s,%s,
            NOW(),
            %s,%s,%s
        )
    """
    
    values=(
        data.get("event_id"),
        data.get("order_id"),
        data.get("customer_id"),
        data.get("product_id"),
        
        data.get("order_status"),
        data.get("payment_type"),
        data.get("price"),
        data.get("quantity"),
        data.get("total_amount"),
        data.get("category"),
        data.get("product_name"),
        # SQL에서 NOW() -> timestamp 생략
        data.get("customer_name"),
        data.get("customer_city"),
        data.get("customer_state")
    )
    
    cur.execute(sql,values)
    conn.commit()
    
def connect_sql_python():
    print("[start] kafka데이터 ->PostgreSQL저장 시작!")
    
    conn=None
    
    try:
        conn=psycopg2.connect(**DB_CONFIG)
        cur=conn.cursor()
        print("DB 연결되었다!")
        
        for message in consumer:
            row=message.value
            insert_data(conn,cur,row)
            print(f"저장 :{row.get('order_id','Unknown')}-{row.get('category','Unknown')}")
            
    except Exception as e:
        print(f"Error!!{e}")
        if conn:
            conn.rollback()
    
    except KeyboardInterrupt:
        print("Stopping..")
        
    finally:
        if conn:
            cur.close()
            conn.close()
            print("DB와의 연결이 끊어졌습니다.")
            
if __name__=="__main__":
    connect_sql_python()