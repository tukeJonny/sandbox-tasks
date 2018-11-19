# -*- coding: utf-8 -*-

from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from datetime import datetime, timedelta

operator_args = {
	'ownrer': 'airflow',
	'depends_on_past': False,
	'start_date': datetime(2018, 11, 20),
	'retries': 3,
	'retry_delay': timedelta(minutes=5),
}

dag = DAG(dag_id='es_cleanup', default_args=operator_args, catchup=False, schedule_interval='0 0 * * 0')

task1 = BashOperator(task_id='delete_older_indices', bash_command='/usr/local/bin/curator /home/airflow/airflow/actions/delete_indices.yml', dag=dag)

if __name__ == '__main__':
	dag.cli()
