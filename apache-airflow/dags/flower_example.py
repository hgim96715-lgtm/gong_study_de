from airflow import DAG
from airflow.datasets import Dataset
from airflow.operators.bash import BashOperator
from datetime import datetime

with DAG(
    dag_id='flower_example',
    schedule='@daily',
    start_date=datetime(2023, 1, 1),
    catchup=False) as dag:
    
    task_producer1=BashOperator(
        task_id="slppe_1",
        bash_command="sleep 20"
    )
    
    task_producer2=BashOperator(
        task_id="slppe_2",
        bash_command="sleep 20"
    )

task_producer1 >> task_producer2