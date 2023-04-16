from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
from datetime import datetime

from twic import TWICClient


def fetch_pgn_from_twic(ds):
    client = TWICClient()
    pgn_content = client.download_pgn_from_date(ds)
    with open(f'/pgns/{ds}.pgn', 'w+') as f:
        f.write(pgn_content)


with DAG(
    dag_id='the_week_in_chess',
    schedule_interval='0 12 * * MON',
    start_date=datetime(2023, 4, 3),
    catchup=False) as dag:

    load_pgn = PythonOperator(
        task_id='load_pgn',
        python_callable=fetch_pgn_from_twic
    )

    