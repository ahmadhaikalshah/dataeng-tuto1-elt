from os import getenv
from subprocess import run
from datetime import datetime

from docker.types import Mount

from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.providers.docker.operators.docker import DockerOperator


default_args = {
    'owner'             : 'airflow',
    'depends_on_past'   : False,
    'email_on_failure'  : False,
    'email_on_entry'    : False
}


elt_dir = getenv('ELT_DIR')


def run_elt_script():
    result = run(
                    [ 'python', f'{elt_dir}/elt_script.py' ],
                    capture_output = True,
                    text = True
                )
    
    if result.returncode != 0:
        raise Exception(f'Script failed with error: {result.stderr}')
    else:
        print(result.stdout)


dag = DAG(
    "elt_and_dbt",
    default_args = default_args,
    description = "An elt workflow with dbt",
    start_date = datetime.now(),
    catchup = False
)


task1 = PythonOperator(
    task_id = 'run_elt_script',
    python_callable = run_elt_script,
    dag = dag
)


task2 = DockerOperator(
    task_id = 'dbt_run',
    image = 'ghcr.io/dbt-labs/dbt-postgres:1.9.latest',
    command = [
        'run',
        '--profiles-dir', '/root',
        '--project-dir', '/dbt',
        '--full-refresh'
    ],
    auto_remove = True,
    docker_url = 'unix://var/run/docker.sock',
    network_mode = 'elt_elt_network',
    mounts = [
        Mount(source = '/home/hitam/dataeng/elt/custom_postgres', target = '/dbt', type= 'bind'),
        Mount(source = '/home/hitam/.dbt', target = '/root', type = 'bind')
    ],
    mount_tmp_dir = False,
    dag = dag
)


task1 >> task2