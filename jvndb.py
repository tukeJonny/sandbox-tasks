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

dag = DAG(dag_id='jvndb', default_args=operator_args, catchup=False, schedule_interval='0 0 * * *')

task1 = BashOperator(task_id='heartbeat_elasticsearch', bash_command='curl -s --fail http://192.168.0.20:9200', dag=dag)

task2_script = """
cd /home/airflow/scrapers/spiderweb-jvndb-crawler
/bin/scrapy crawl jvndb
"""
task2 = BashOperator(task_id='crawl', bash_command=task2_script, dag=dag)

task2.set_downstream(task1)

if __name__ == '__main__':
	dag.cli()
