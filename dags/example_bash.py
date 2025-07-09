from datetime import datetime, timedelta

from airflow import DAG
from airflow.providers.standard.operators.bash import BashOperator

default_args = {
    "owner": "marco",
    "retries": 2,
    "retry_delay": timedelta(minutes=2)
}

with DAG(
    dag_id="example_dag",
    default_args=default_args,
    description="example dag for experimentation",
    start_date=datetime(2024, 7, 9, 0),
    schedule="@daily"
) as dag:
    task_1 = BashOperator(
        task_id="first_task",
        bash_command="echo hello world"
    )

    task_2 = BashOperator(
        task_id="second_task",
        bash_command="echo I run after task 1"
    )

    task_3 = BashOperator(
        task_id="third_task",
        bash_command="echo I run after task 1, with task 2"
    )

# task dependencies
task_1.set_downstream(task_2)
task_1.set_downstream(task_3)

# alternative syntax
# task_1 >> task_2
# task_1 >> task_3

# or...
# task_1 >> [task_2, task_3]