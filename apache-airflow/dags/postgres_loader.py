from airflow import DAG
# 기존 PostgresOperator 대신 SQLExecuteQueryOperator 사용(범용)
from airflow.providers.common.sql.operators.sql import SQLExecuteQueryOperator
from airflow.providers.common.sql.sensors.sql import SqlSensor
from datetime import datetime

with DAG(
    dag_id="postgres_loader",
    start_date=datetime(2026, 1, 1),
    schedule=None,
    catchup=False) as dag:

        
    create_table = SQLExecuteQueryOperator(
        task_id="create_sample_table",
        # postgres_conn_id 대신 범용 커넥션 아이디 사용
        conn_id="my_postgres_connection",
        sql="""
        CREATE TABLE IF NOT EXISTS sample_table (
            key TEXT,
            value TEXT
        );
        """
    )

    insert_data = SQLExecuteQueryOperator(
        task_id="insert_sample_data",
        # postgres_conn_id 대신 범용 커넥션 아이디 사용
        conn_id="my_postgres_connection",
        sql="""
        INSERT INTO sample_table (key, value)
        VALUES ('my', 'connection');
        """
    )
    sql_sensor=SqlSensor(
        task_id='wait_for_condition',
        conn_id='my_postgres_connection',
        sql="SELECT COUNT(*) FROM sample_table WHERE key='my'",
        mode='poke',
        poke_interval=30
    )
    sql_query_confirm="""
        INSERT INTO sample_table(key,value)
        VALUES('sensor','confirmed');
    """
    postres_confirm_task=SQLExecuteQueryOperator(
        task_id='execute_sql_confirm_query',
        conn_id='my_postgres_connection',
        sql=sql_query_confirm
    )

    create_table >> insert_data >> sql_sensor >> postres_confirm_task
