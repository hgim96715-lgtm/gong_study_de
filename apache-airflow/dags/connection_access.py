
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.hooks.base import BaseHook
import pendulum

def _access_connection(ti):
    print("Fetching connection info...")
    print(BaseHook.get_connection('my_postgres_connection').host)
    print(BaseHook.get_connection('my_postgres_connection').password)
    print("ended")

with DAG(
    dag_id='connection_access',
    start_date=pendulum.datetime(2026,1,20, tz="Asia/Seoul"),
):
    task_extract_data_op=PythonOperator(
        task_id="extract_data_op",
        python_callable=_access_connection
    )
    
