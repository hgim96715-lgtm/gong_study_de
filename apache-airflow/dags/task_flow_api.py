from airflow.decorators import dag, task
import pendulum

@dag(
    dag_id='task_flow_api',
    schedule='@daily',
    start_date=pendulum.datetime(2023, 1, 1, tz="Asia/Seoul"),
    catchup=False
)

def task_flow_api_dag():
    
    # [Task 1] 데이터 추출 (Dict 리턴 -> 자동으로 XCom Push)
    @task
    def extract():
        data={'orders': [100, 200, 300]}
        print(f"Extracted data: {data}")
        return data
    
    # [Task 2] 데이터 변환 (인자로 받음 -> 자동으로 XCom Pull)
    @task
    def transform(data):
        transformed_data={'total_orders':sum(data['orders'])}
        print(f"Transformed data: {transformed_data}")
        return transformed_data
    
    # [Task 3] 데이터 적재
    @task
    def load(data):
        print(f"Loading data: {data}")
        
    raw_data=extract()
    processed_data=transform(raw_data)
    load(processed_data)

etl_dag=task_flow_api_dag()