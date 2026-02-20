from pyflink.table import EnvironmentSettings,TableEnvironment
from pyflink.table.window import Tumble
from pyflink.table.expressions import col,lit

def real_time_aggregation():
    settings=EnvironmentSettings.in_streaming_mode()
    t_env=TableEnvironment.create(settings)
    
    print(">>> PyFlink Start!!")
    
    
    
    t_env.execute_sql("""
                      CREATE TABLE source_table(
                          order_id STRING,
                          total_amount BIGINT,
                          category STRING,
                          
                          `timestamp` TIMESTAMP(3),
                          
                          WATERMARK FOR `timestamp` AS `timestamp` - INTERVAL '5' SECOND
                          ) WITH(
                              'connector'='kafka',
                              'topic'='user-log',
                              'properties.bootstrap.servers'='kafka:9092',
                              'properties.group.id'='project-flik-aggregator-dev',
                              'scan.startup.mode'='latest-offset',
                              'format'='json',
                              'json.timestamp-format.standard' = 'ISO-8601'
                              )""")
    
    agg_query="""
        SELECT
            window_start,
            window_end,
            category,
            SUM(total_amount) as total_sales,
            COUNT(order_id) as total_orders
        FROM TABLE(
            TUMBLE(TABLE source_table,DESCRIPTOR(`timestamp`),INTERVAL '1' MINUTE)
        )
        GROUP BY window_start,window_end,category"""
        
    
    t_env.execute_sql("""
                      CREATE TABLE jdbc_sink(
                          window_start TIMESTAMP(3),
                          window_end TIMESTAMP(3),
                          category STRING,
                          total_sales BIGINT,
                          total_orders BIGINT
                      ) WITH(
                          'connector'='jdbc',
                          'url'='jdbc:postgresql://postgres:5432/airflow',
                          'table-name'='sales_aggregation',
                          'username'='airflow',
                          'password'='airflow',
                          'driver'='org.postgresql.Driver'
                      )
                """)
    
    t_env.execute_sql(f"INSERT INTO jdbc_sink {agg_query}")
    
if __name__=='__main__':
    real_time_aggregation()
    