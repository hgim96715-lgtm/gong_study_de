from airflow import DAG 
from airflow.operators.empty import EmptyOperator
import pendulum

# normal way
# with DAG('list_task_dag', start_date=pendulum.datetime(2026,1,20, tz="Asia/Seoul"),depends_on_past=False,owner='airflow') as dag:
#     task1 = EmptyOperator(task_id='task1')
#     task2 = EmptyOperator(task_id='task2')
#     task3 = EmptyOperator(task_id='task3')


default_args={
    'owner':'airflow',
    'depends_on_past':False,
    'start_date':pendulum.datetime(2026,1,20, tz="Asia/Seoul"),
}

with DAG(
    dag_id='default_argument',
    default_args=default_args,
):
    task1 = EmptyOperator(task_id='task1')
    task2 = EmptyOperator(task_id='task2')
    task3 = EmptyOperator(task_id='task3')

    task1 >> task2 >> task3