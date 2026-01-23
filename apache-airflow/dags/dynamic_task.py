import pendulum
from airflow import DAG
from airflow.operators.empty import EmptyOperator

with DAG(
    dag_id='dynamic_task',
    start_date=pendulum.datetime(2026,1,20, tz="Asia/Seoul"),
    catchup=False,
) as dag:
    tasks=[]
    for i in range(0,5):
        tasks.append(EmptyOperator(task_id=f'task{i}'))
        if i !=0:
            tasks[i-1] >> tasks[i]