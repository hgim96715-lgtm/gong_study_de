# airflow.operators.dummy -> airflow.operators.empty 로 변경됨
from airflow import DAG
from airflow.operators.empty import EmptyOperator
from airflow.operators.python import PythonOperator
from datetime import datetime

def print_hello():
    print('우와! Airflow다!')

with DAG('my_first_dag',
         description='나의 첫번째 Airflow DAG',
         # 매일 자정에 실행
         # schedule_interval -> schedule 로 변경됨
         schedule='0 0 * * *',
         start_date=datetime(2026,1,19),
         # catchup : 이전 날짜의 DAG 실행 여부 설정, 기본값 True
         catchup=False) as dag:
    
    task1=PythonOperator(
        task_id='print_hello_task',
        # 함수를 실행할때는 () 붙이지 않음
        python_callable=print_hello,
        dag=dag
    )
    # Dummy Operator -> Empty Operator 로 변경됨
    # 실제 작업은 안하지만, 워크플로우 상에서의 흐름을 나타내기 위해 사용
    task2=EmptyOperator(
        task_id='dummy_task',
        dag=dag
    )
    
task1 >> task2