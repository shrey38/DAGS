from datetime import datetime

from airflow import DAG
from airflow.operators.python import PythonOperator


def celery_task():
    print("This task is executed by the Celery worker.")
    print("Execution path: CeleryKubernetesExecutor -> Celery -> Redis -> Worker")


def kubernetes_task():
    print("This task is executed as a dedicated Kubernetes pod.")
    print("Execution path: CeleryKubernetesExecutor -> KubernetesExecutor -> Pod")


with DAG(
    dag_id="celery_kubernetes_demo",
    start_date=datetime(2024, 1, 1),
    schedule=None,
    catchup=False,
    tags=["demo", "celery", "kubernetes"],
) as dag:

    celery_task = PythonOperator(
        task_id="celery_task",
        python_callable=celery_task,
    )

    kubernetes_task = PythonOperator(
        task_id="kubernetes_task",
        python_callable=kubernetes_task,
        queue="kubernetes",
    )

    celery_task >> kubernetes_task
