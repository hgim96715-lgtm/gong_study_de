import pendulum
from time import time
from airflow import DAG
from airflow.operators.empty import EmptyOperator
from airflow.operators.python import BranchPythonOperator

def decide_which_path():
    if int(time()) % 2==0:
        print(f"지금 시간은 짝수입니다. {int(time())}")
        return "even_path_task"
    else:
        print(f"지금 시간은 홀수입니다. {int(time())}")
        return "odd_path_task"
    
with DAG(
    dag_id='branch_dag',
    start_date=pendulum.datetime(2026,1,1),
    schedule='@hourly',
    default_args={"retries":1},
    catchup=False
) as dag:
    
    branch_task=BranchPythonOperator(
        task_id='branching_task',
        python_callable=decide_which_path 
    )
    
    even_path_task=EmptyOperator(task_id='even_path_task')
    odd_path_task=EmptyOperator(task_id='odd_path_task')
    
branch_task >>even_path_task
branch_task >>odd_path_task