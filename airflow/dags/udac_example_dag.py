from datetime import datetime, timedelta
import os
from airflow import DAG, macros
from airflow.operators.postgres_operator import PostgresOperator
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators import (StageToRedshiftOperator, LoadFactOperator,
                                LoadDimensionOperator, DataQualityOperator)
from helpers import SqlQueries
default_args = {
    'owner': 'gabriel',
    'start_date': datetime(2021, 5, 17),
    'end_date': datetime(2021, 5, 23),
    'depends_on_past': False,
    'retries': 0,
    'retry_delay': timedelta(minutes=120),
    'catchup': False,
    'email_on_retry': False
}

dag = DAG('pinngo_capstone_2',
          default_args=default_args,
          description='Load and transform data in Redshift with Airflow',
          schedule_interval='0 23 * * *'
        )
execution_date = '{{ execution_date }}'
print(execution_date)
start_operator = DummyOperator(task_id='Begin_execution',  dag=dag)

create_tables_redshift = PostgresOperator(
    task_id="create_tables",
    dag=dag,
    postgres_conn_id="redshift",
    sql='create_tables.sql'
)

stage_categories_to_redshift = StageToRedshiftOperator(
    task_id='Stage_categories',
    dag=dag,
    redshift_conn_id = "redshift",
    aws_credentials_id = "aws_credentials",
    table = "app_categoria_nielsen",
    s3_bucket = "udacity-capstone-pinngo",
    s3_key = "app_categoria_nielsen_202106131609.json",
    format_file = "JSON",
    operation = "delete"
)

stage_empresa_to_redshift = StageToRedshiftOperator(
    task_id='Stage_empresa',
    dag=dag,
    redshift_conn_id = "redshift",
    aws_credentials_id = "aws_credentials",
    table = "empresa_report",
    s3_bucket = "udacity-capstone-pinngo",
    s3_key = "empresa_report_202106131755.csv",
    format_file = "csv",
    operation = "delete"
)

stage_produto_to_redshift = StageToRedshiftOperator(
    task_id='Stage_produto',
    dag=dag,
    redshift_conn_id = "redshift",
    aws_credentials_id = "aws_credentials",
    table = "app_produto",
    s3_bucket = "udacity-capstone-pinngo",
    s3_key = "app_produto_202106131757.csv",
    format_file = "csv",
    operation = "delete"
)

stage_ean_genuino_to_redshift = StageToRedshiftOperator(
    task_id='Stage_ean_genuino',
    dag=dag,
    redshift_conn_id = "redshift",
    aws_credentials_id = "aws_credentials",
    table = 'app_ean_genuino_weekly',
    s3_bucket = "udacity-capstone-pinngo",
    s3_key = "shopping-receipts/app_ean_genuino_weekly_"+"{{ ds }}"+".csv",
    format_file = "csv",
    delimiter = ',',
    operation = "append"
)

load_categories_redshift = LoadDimensionOperator (
    task_id='Load_categories_dim_table',
    dag=dag,
    redshift_conn_id='redshift',
    table='categories_dim',
    sql_query=SqlQueries.categories_insert,
    append=True    
)

load_cities_redshift = LoadDimensionOperator (
    task_id='Load_cities_dim_table',
    dag=dag,
    redshift_conn_id='redshift',
    table='city_dim',
    sql_query=SqlQueries.dimcity_insert,
    append=True    
)

load_times_redshift = LoadDimensionOperator (
    task_id='Load_times_dim_table',
    dag=dag,
    redshift_conn_id='redshift',
    table='time_dim',
    sql_query=SqlQueries.time_insert,
    append=True    
)

load_fact_redshift = LoadFactOperator (
    task_id='Load_fact_table',
    dag=dag,
    redshift_conn_id='redshift',
    table='product_sales',
    sql_query=SqlQueries.product_sales_insert)

end_operator = DummyOperator(task_id='Stop_execution',  dag=dag)

start_operator >> create_tables_redshift
create_tables_redshift >> stage_categories_to_redshift
create_tables_redshift >> stage_empresa_to_redshift
create_tables_redshift >> stage_produto_to_redshift
create_tables_redshift >> stage_ean_genuino_to_redshift
stage_categories_to_redshift >> load_categories_redshift
stage_empresa_to_redshift >> load_cities_redshift
stage_ean_genuino_to_redshift >> load_times_redshift
stage_produto_to_redshift >> load_fact_redshift
stage_empresa_to_redshift >> load_fact_redshift
stage_ean_genuino_to_redshift >> load_fact_redshift
load_fact_redshift >> end_operator
load_times_redshift >> end_operator
load_cities_redshift >> end_operator
load_categories_redshift >> end_operator

