from airflow import DAG
from airflow.operators.python import PythonOperator
from environment_operators.start_environment import StartEnvironmentOperator
from environment_operators.run_python_script import RunPythonScriptOperator
from environment_operators.stop_environment import StopEnvironmentOperator
from environment_operators.strategies import EnvironmentStrategyEnum
from datetime import datetime
import os


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
            'image_name': 'twic',
            'volumes': {
                "D:\chess-etl/pgns": "/pgns"
            }
        }
    )

    load_pgn = RunPythonScriptOperator(
        task_id='load_pgn',
        strategy=EnvironmentStrategyEnum.SIBLING_DOCKER,
        strategy_args={
            'container_name': f'twic-{exec_date}'
        },
        script_path='load_pgn_from_twic.py',
        script_args=[exec_date]
    )

    stop_environment = StopEnvironmentOperator(
        task_id='stop_environment',
        strategy=EnvironmentStrategyEnum.SIBLING_DOCKER,
        strategy_args={
            'container_name': f'twic-{exec_date}'
        }
    )

    start_environment >> load_pgn >> stop_environment
    