from datetime import datetime, timedelta

from airflow import DAG
from airflow.providers.standard.operators.python import PythonOperator

default_args = {
    "owner": "marco",
    "retries": 2,
    "retry_delay": timedelta(minutes=2)
}

def greet(ti):
    first_name = ti.xcom_pull(task_ids="get_name", key="first_name")
    last_name = ti.xcom_pull(task_ids="get_name", key="last_name")
    age = ti.xcom_pull(task_ids="get_age", key="age")
    print(f"hello world! my name is {first_name} {last_name} and i'm {age} years old")

def get_name(ti):
    ti.xcom_push(key="first_name", value="shaggy")
    ti.xcom_push(key="first_name", value="rogers")

def get_age(ti):
    ti.xcom_push(key="age", value=56)

with DAG(
    dag_id="example_python_dag",
    default_args=default_args,
    description="example dag with python operator",
    start_date=datetime(2024, 7, 9, 0),
    schedule="@daily"
) as dag:
    task_1 = PythonOperator(
        task_id="greet",
        python_callable=greet
        # op_kwargs={"age": 56}
    )

    task_2 = PythonOperator(
        task_id="get_name",
        python_callable=get_name
    )

    task_3 = PythonOperator(
        task_id="get_age",
        python_callable=get_age
    )

    [task_2, task_3] >> task_1