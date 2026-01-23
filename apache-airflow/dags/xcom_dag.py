import random
import pendulum
from airflow import DAG
from airflow.decorators import task



with DAG(
    dag_id='xcom_dag',
    start_date=pendulum.datetime(2023, 1, 1),
    schedule='@daily',
    default_args={"retries":1},
) as dag:
    
    @task
    def generate_number():
        number=random.randint(1,100)
        print(f"Generated number: {number}")
        return number
        
    @task    
    def read_number(number):
        print(f"Read number: {number}")
        
    read_number(generate_number())
    