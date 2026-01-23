from airflow import DAG
from airflow.operators.empty import EmptyOperator
import pendulum

with DAG(
    dag_id='list_task_dag',
    start_date=pendulum.datetime(2026,1,20, tz="Asia/Seoul")
) as dag:
    task1 = EmptyOperator(task_id='task1')
    task2 = EmptyOperator(task_id='task2')
    task3 = EmptyOperator(task_id='task3')
    task4 = EmptyOperator(task_id='task4')
    task5 = EmptyOperator(task_id='task5')
    
# normal way
# task1 >> task2
# task1 >> task3
# task1 >> task4
# task2 >> task5
# task3 >> task5
# task4 >> task5

task1 >>[task2,task3,task4] >> task5