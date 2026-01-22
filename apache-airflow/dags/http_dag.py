import json
from datetime import datetime

from airflow import DAG
from airflow.providers.http.operators.http import HttpOperator
from airflow.providers.common.sql.operators.sql import SQLExecuteQueryOperator
from airflow.operators.python import PythonOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook

from pandas import json_normalize

def _extract_date(**context):
    response=context['ti'].xcom_pull(task_ids='get_op')
    starwars_character=json_normalize({
        "name":response['name'],
        "height":response['height'],
        "mass":response['mass']
    })

    starwars_character.to_csv("/tmp/starwars_character.csv",header=False,index=None)

def _store_character(**context):
    hook=PostgresHook(
        postgres_conn_id='my_postgres_connection'
    )
    hook.copy_expert(
        filename="/tmp/starwars_character.csv",
        sql="COPY starwars_character FROM stdin WITH DELIMITER as ','"
    )
with DAG('http_dag',
         description='http dag',
         schedule='0 0 * * *',
         start_date=datetime(2026,1,10),
         catchup=False) as dag:
    
    task_create_table_op=SQLExecuteQueryOperator(
        task_id="create_table_op",
        conn_id='my_postgres_connection',
        sql='''
            CREATE TABLE IF NOT EXISTS starwars_character(
                name TEXT NOT NULL,
                height TEXT NOT NULL,
                mass TEXT NOT NULL
            )
        '''
    )
    
    task_get_op=HttpOperator(
        task_id="get_op",
        http_conn_id='my_http_connection',
        endpoint="/api/people/1/",
        headers={"Content-Type":"application/json"},
        method='GET',
        response_filter=lambda response:json.loads(response.text),
        log_response=True
    )
    
    task_extract_data_op=PythonOperator(
        task_id="extract_data_op",
        python_callable=_extract_date,
    )
    
    task_store_op=PythonOperator(
        task_id="store_op",
        python_callable=_store_character,
    )
    
task_create_table_op >> task_get_op >> task_extract_data_op >> task_store_op