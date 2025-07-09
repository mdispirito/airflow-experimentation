from datetime import datetime, timedelta

from airflow.decorators import dag, task

default_args = {
    "owner": "marco",
    "retries": 2,
    "retry_delay": timedelta(minutes=2)
}

@dag(
    dag_id="taskflow_example_dag",
    default_args=default_args,
    start_date=datetime(2024, 7, 9, 0),
    schedule="@daily"
)
def hello_world_etl():
    
    @task(multiple_outputs=True)
    def get_name():
        return {
            "first_name": "scooby",
            "last_name": "doo"
        }

    @task()
    def get_age():
        return 56
    
    @task()
    def greet(first_name, last_name, age):
        print(f"hello world! my name is {first_name} {last_name} and i'm {age} years old")

    names = get_name()
    age = get_age()
    greet(first_name=names["first_name"], last_name=names["last_name"], age=age)

greet_dag = hello_world_etl()
