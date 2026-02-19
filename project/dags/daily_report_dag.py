from airflow import DAG
from airflow.providers.docker.operators.docker import DockerOperator
from datetime import datetime,timedelta
import pendulum
from docker.types import Mount
from airflow.models import Variable


default_args={
    'owner':'airflow',
    'start_date':datetime(2026,2,17),
    'retries':2,
    'retry_delay':timedelta(minutes=5)
}

with DAG(
    dag_id='daily_report_dag',
    default_args=default_args,
    schedule_interval='@daily',
    start_date=pendulum.datetime(2026, 2, 17, tz='Asia/Seoul'),
    catchup=False
)as dag:
    
    run_spark_job=DockerOperator(
        task_id='run_spark_daily_report',
        image='project-spark-worker:latest',
        api_version='auto',
        auto_remove=True,
        network_mode='project_data-network',
        mount_tmp_dir=False,
        environment={
            'DB_HOST': Variable.get("daily_report_db_host", default_var=""),
            'DB_PORT':'5432',
            'DB_NAME':'airflow',
            'DB_USER':'airflow',
            'DB_PASSWORD': Variable.get("daily_report_db_pwd", default_var="")
            
        },
        command="/opt/spark/bin/spark-submit --master spark://spark-master:7077 --jars /opt/spark/drivers/postgresql-42.7.1.jar /opt/spark/apps/daily_report.py",
        
        mounts=[
            Mount(
                source="/Users/gong/gong_study_de/project/spark_app",
                target="/opt/spark/apps",
                type='bind'
            ),
            Mount(
                source="/Users/gong/gong_study_de/project/spark_drivers",
                target="/opt/spark/drivers",
                type='bind'
            )
        ]
        
    )