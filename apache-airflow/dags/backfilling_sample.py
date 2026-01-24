import pendulum
from airflow.decorators import dag, task

@dag(
    dag_id='backfilling_sample',
    schedule='@daily',  
    start_date=pendulum.datetime(2026, 1, 2, tz="America/New_York"),
    catchup=False,
)
def backfilling_sample():

    @task(retries=3)
    def print_context():
        print("Hello")
        # raise Exception("Backfill Exception")

    print_context()

backfilling_sample()
