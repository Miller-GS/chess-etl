from airflow import DAG
from airflow.operators.python import PythonOperator
from environment_operators.start_environment import StartEnvironmentOperator
from environment_operators.stop_environment import StopEnvironmentOperator
from environment_operators.strategies import EnvironmentStrategyEnum
from datetime import datetime
from twic import TWICClient
import os


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

    exec_date = '{{ ds }}'
    start_environment = StartEnvironmentOperator(
        task_id='start_environment',
        strategy=EnvironmentStrategyEnum.SIBLING_DOCKER,
        strategy_args={
            'docker_file_path': os.path.join(os.path.dirname(__file__), 'jobs'),
            'container_name': f'twic-{exec_date}',
            'image_name': 'twic'
        }
    )

    load_pgn = PythonOperator(
        task_id='load_pgn',
        python_callable=fetch_pgn_from_twic
    )

    stop_environment = StopEnvironmentOperator(
        task_id='stop_environment',
        strategy=EnvironmentStrategyEnum.SIBLING_DOCKER,
        strategy_args={
            'container_name': f'twic-{exec_date}'
        }
    )

    start_environment >> load_pgn >> stop_environment
    