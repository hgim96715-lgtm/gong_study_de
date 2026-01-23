from datetime import datetime
from airflow import DAG
from airflow.decorators import task_group
from airflow.operators.bash import BashOperator
from airflow.operators.empty import EmptyOperator
from airflow.utils.edgemodifier import Label


with DAG(
    dag_id='task_group',
    start_date=datetime(2023, 12, 1),
    schedule='@daily',
    default_args={"retries":1},
    catchup=False) as dag:
    
    @task_group(default_args={"retries":3})
    def group1():
        """This docstring will become the tooltip for the TaskGroup."""
        task1=EmptyOperator(task_id='task1')
        task2=BashOperator(
            task_id="task2",
            bash_command="echo Hello World",
            retries=2
        )
        print(task1.retries)  
        print(task2.retries)  
        
    task3=EmptyOperator(task_id='task3')
    
    # TaskGroup 안 병렬 실행 → Label → task3 순서
    group1() >> Label("When completed")>> task3