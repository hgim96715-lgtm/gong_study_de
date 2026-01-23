from airflow import DAG
from airflow.operators.bash import BashOperator
import pendulum

params={
    "p1":"v1",
    "p2":"v2",
}

with DAG(
    dag_id='params_argument',
    start_date=pendulum.datetime(2024,6,20, tz="Asia/Seoul"),
    params=params,
    catchup=False 
) as dag:
    
    task1=BashOperator(
        task_id='task1',
        bash_command='echo {{params.p1}}'
    )
    
    task2=BashOperator(
        task_id='task2',
        bash_command='echo {{params.p2}} {{params.p3}}',
        params={"p3":"v3"}
    )
    task1 >> task2