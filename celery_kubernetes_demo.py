from datetime import datetime
import time

from airflow import DAG
from airflow.operators.python import PythonOperator


def celery_task():
    print("=== CELERY EXECUTION ===")
    print("Task: celery_task")
    print("Executor: CeleryKubernetesExecutor")
    print("Queue: default")
    print("Execution: Celery -> Redis -> Celery Worker")
    time.sleep(30)


def kubernetes_task():
    print("=== KUBERNETES EXECUTION ===")
    print("Task: kubernetes_task")
    print("Executor: CeleryKubernetesExecutor")
    print("Queue: kubernetes")
    print("Execution: KubernetesExecutor -> Dedicated Kubernetes Pod")
    time.sleep(30)


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
