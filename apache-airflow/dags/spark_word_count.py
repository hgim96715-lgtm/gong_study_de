from airflow.decorators import dag
from airflow.providers.amazon.aws.sensors.s3 import S3KeySensor
from airflow.providers.apache.spark.operators.spark_submit import SparkSubmitOperator
import pendulum

# 기본 설정
default_args = {
    "owner": "airflow",
    'start_date': pendulum.datetime(2026, 1, 20, tz="Asia/Seoul"),
    "retries": 1,
}

@dag(
    default_args=default_args,
    schedule=None,      # 수동 실행 (원하면 '@daily' 등으로 변경)
    catchup=False,
    tags=['spark', 'minio'],
)
def spark_word_count_taskflow():

    # 1. 감시자: MinIO에 파일이 있나 확인 (Sensor)
    check_minio_file = S3KeySensor(
        task_id='check_minio_file',
        bucket_name='airflow-minio',       # ⭐️ 우리 버킷 이름
        bucket_key='input.txt',            # 감시할 파일명
        aws_conn_id='minio_default',       # 아까 만든 연결 ID
        poke_interval=10,                  # 10초마다 확인
        timeout=60 * 5                     # 5분 동안 안 오면 포기
    )

    # 2. 실행자: Spark에게 일 시키기 (Operator)
    spark_task = SparkSubmitOperator(
task_id="spark_submit_task",
        conn_id="spark_default",
        application='/opt/airflow/dags/word_count_app.py',
        
        # 👇 [핵심 수정] 설정을 여기서 강제로 주입합니다!
        packages="org.apache.hadoop:hadoop-aws:3.3.4,com.amazonaws:aws-java-sdk-bundle:1.12.262",
        conf={
            # 1. 돌아오는 길(Callback) 설정
            "spark.driver.bindAddress": "0.0.0.0",
            "spark.driver.host": "host.docker.internal",  # Mac에서는 이게 정답입니다
            "spark.driver.port": "20000",
            "spark.blockManager.port": "20001",
            
            # 2. MinIO 설정 (DAG에서 강제 지정하면 확실함)
            "spark.hadoop.fs.s3a.endpoint": "http://minio:9000",
            "spark.hadoop.fs.s3a.access.key": "ROOTNAME",
            "spark.hadoop.fs.s3a.secret.key": "CHANGEME123",
            "spark.hadoop.fs.s3a.path.style.access": "true",
            "spark.hadoop.fs.s3a.impl": "org.apache.hadoop.fs.s3a.S3AFileSystem",
            "spark.hadoop.fs.connection.ssl.enabled": "false",
        },
        
        # 👇 [핵심 수정] Java 위치를 강제로 알려줍니다.
        env_vars={"JAVA_HOME": "/usr/lib/jvm/java-17-openjdk-arm64"},
        
        application_args=[
            "s3a://airflow-minio/input.txt", 
            "s3a://airflow-minio/output_airflow"
        ]
    )

    # 3. 순서 연결 (Sensor가 성공하면 -> Spark 실행)
    check_minio_file >> spark_task

# DAG 생성
spark_dag = spark_word_count_taskflow()