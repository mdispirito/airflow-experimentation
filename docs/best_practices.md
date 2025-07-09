Best Practices
- Keep DAG files small and focused on orchestration, not business logic.
- Ensure Tasks are Idempotent (important for retries or backfills)
- Tasks should be single-purpose
- Try to stick to `catchup=False` to avoid hundreds of backfill runs unintentionally
- Store sensitive credentials in airflow connections, not in code
- Keep DAG parsing fast by avoiding any slow code or excessive imports in DAGs

Separation of Business Logic and Orchestration Logic

1 Put business logic in a script, ex:
```python
def run():
    import psycopg2
    conn = psycopg2.connect(...)  # use environment variables or Airflow connections
    with conn.cursor() as cur:
        cur.execute("SELECT * FROM source_table")
        rows = cur.fetchall()
        for row in rows:
            cur.execute("INSERT INTO target_table ...", ...)
    conn.commit()
    conn.close()
```

2 Call the business logic from the Operator
```python
from airflow.operators.python import PythonOperator
from data_tasks.transform_users import run

transform_task = PythonOperator(
    task_id='transform_users',
    python_callable=run,
    dag=dag,
)
```

3 The task code then runs on a worker, which is part of the Airflow infra. It depends which worker type you select.
- Local Executors - share resources with the scheduler!
	- LocalExecutor - same machine as scheduler. Okay for simple setups but not great for larger scale prod.
Remote Executors
- Queued/Batch Executors - tasks are sent to a central queue. Decouples workers from scheduler, but shared workers also have noisy neighbour problem.
	- CeleryExecutor - On distributed Celery worker containers - scales better in prod.
	- BatchExecutor
- Containerized Executors - tasks executed ad-hoc inside containers/pods. No noisy neighbours and customized environment for each tasks. Downside is latency/startup for each pod and cost of many small tasks.
	- KubernetesExecutor - Runs in dedicated, ephemeral (short-lived) K8s pod - best isolation and scalability, but increased complexity.
	- EcsExecutor

Airflow Docker Image Extension vs Customization
- Extending
	- good for 99% of cases
	- just add additional requirements to your dockerfile, rebuild the image and go
	- easy and fast to build
- Image Customization
	- Needed if you care about optimizing image size
	- need to copy the airflow source and then customize it, and rebuild image from source
	- might be needed if you need to build the image in an air-gapped system
