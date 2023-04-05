import datetime as dt
from pytz import timezone

from airflow import DAG 
from airflow.operators.python import PythonOperator

def extract(ti):
    with open('/path/to/file/etl_text.txt', 'r') as f:
        data = f.read()
        print('DATA IN EXTRACT FUNC:',data)
        ti.xcom_push(key='extract_val', value=data)
    
def transform(ti):
    word_count = 0
    extract_val = ti.xcom_pull(key='extract_val', task_ids=['extract_opr'])
    print("ALL DATA IN TRANSFORM FUNC:",extract_val)
    for x in extract_val:
        print("X in LOOP:",x)
        word_count += 1
        print("WORD COUNT IN LOOP:", word_count)
    ti.xcom_push(key='transform_val', value=word_count)

def load(ti):
    word_int = ti.xcom_pull(key='transform_val', task_ids=['transform_opr'])
    word_int = str(word_int)
    print("WORD INT IN LOAD FUNC:", word_int)
    with open('/path/to/file/etl_text.txt', 'a+') as f:
        f.write(word_int)

tz = timezone('Africa/Nairobi')

default_args = {'retries':0}

with DAG (
    'etl_test',
    default_args=default_args,
    schedule = '*/10 * * * *',
    start_date= dt.datetime(2023, 3, 29, 7 , 20, 00, tzinfo=tz)
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