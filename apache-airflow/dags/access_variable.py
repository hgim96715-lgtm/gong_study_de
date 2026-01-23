from airflow import DAG
from airflow.operators.python import PythonOperator
import pendulum
from airflow.models import Variable

def _access_variable(ti):
    print("Fetching variable info...")
    var_dict=Variable.get("var_dict", deserialize_json=True)
    print(var_dict['key1'])
    print(var_dict['key2'])
    print("ended")
    
with DAG(
    dag_id='access_variable',
    start_date=pendulum.datetime(2026,1,20, tz="Asia/Seoul"),
):
    task_extract_data_op=PythonOperator(
        task_id="extract_data_op",
        python_callable=_access_variable
    )