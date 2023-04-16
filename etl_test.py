import datetime as dt
from pytz import timezone

"""Importing the necessary modules for the ETL DAG"""
from airflow import DAG 
from airflow.operators.python import PythonOperator

"""Defining the extract function to extract text from a file in the local file system"""
def extract(ti):
    with open('/path/to/file/etl_text.txt', 'r') as f:
        data = f.read()
        print('DATA IN EXTRACT FUNC:',data)
        ti.xcom_push(key='extract_val', value=data)
    
"""Defining the transform function to count the number of words in the text file"""
def transform(ti):
    word_count = 0
    extract_val = ti.xcom_pull(key='extract_val')
    print("ALL DATA IN TRANSFORM FUNC:",extract_val)
    word_count = len(extract_val.split())
    print("WORD COUNT IN TRANSFORM FUNC:",word_count,"words")
    ti.xcom_push(key='transform_val', value=word_count)

"""Defining the load function to load the word count into the same file"""
def load(ti):
    word_int = ti.xcom_pull(key='transform_val')
    word_int = str(word_int)
    print("WORD INT IN LOAD FUNC:", word_int)
    with open('/path/to/file/etl_text.txt', 'a+') as f:
        f.write(word_int)

tz = timezone('Africa/Nairobi')

"""Defining the DAG"""
default_args = {'retries':0}

with DAG (
    'etl_test',
    default_args=default_args,
    schedule = '*/10 * * * *',
    start_date= dt.datetime(2023, 3, 29, 7 , 20, 00, tzinfo=tz)
    catchup=False
    ) as dag:
    extract_opr = PythonOperator(
        task_id = "extract",
        python_callable = extract
    )
    transform_opr = PythonOperator(
        task_id = "transform",
        python_callable = transform
    )
    load_opr = PythonOperator(
        task_id = "load",
        python_callable= load
    )

extract_opr >> transform_opr >> load_opr
