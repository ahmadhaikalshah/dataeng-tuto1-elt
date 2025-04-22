from datetime import datetime
from os import getenv
from subprocess import run

from docker.types import Mount

from airflow import DAG

from airflow.operators.python_operator import PythonOperator
from airflow.operators.bash import BashOperator

from airflow.providers.docker.operators.docker import DockerOperator


default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_entry': False
}


hostname = getenv('HOSTNAME')
port_no = int(getenv('PORT_NO'))
elt_dir = getenv('ELT_DIR')


# def run_elt_script():
#     result = run(
#         [ 'python', f'{elt_dir}/elt_script.py' ],
#         capture_output = True,
#         text = True
#         )
    
#     if result.returncode != 0:
#         raise Exception(f'Script failed with error: {result.stderr}')
#     else:
#         print(result.stdout)


dag = DAG(
    'elt_and_dbt',
    default_args = default_args,
    description = 'An elt workflow with dbt',
    start_date = datetime.now(),
    catchup = False
)


# t1 = PythonOperator(
#     task_id = 'run_elt_script',
#     python_callable = run_elt_script,
#     dag = dag
# )
t1 = BashOperator(
    task_id = 'run_elt_script',
    bash_command = f'/bin/bash {elt_dir}/start.sh',
    dag = dag
)


t2 = DockerOperator(
    task_id = 'dbt_run',
    image = 'ghcr.io/dbt-labs/dbt-postgres:1.9.latest',
    entrypoint = '/bin/sh',
    command = f"""
        -c '
        echo "Installing bash and curl...";
        apt-get update;
        apt-get install bash;
        apt-get install -y curl;
        echo "Waiting for ELT script to complete...";
        until curl --silent --fail http://{hostname}:{port_no}; do
            echo "Still waiting...";
            sleep 2;
        done;
        echo "ELT done. Running DBT...";
        dbt run --profiles-dir /root --project-dir /dbt --full-refresh;
        '
    """,
    auto_remove = True,
    docker_url = 'unix://var/run/docker.sock',
    network_mode = 'bridge',
    mounts = [
        Mount(source = './custom_postgres', target = '/dbt', type= 'bind'),
        Mount(source = '~/.dbt', target = '/root', type = 'bind')
    ],
    dag = dag
)


t1 >> t2