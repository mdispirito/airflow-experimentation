# airflow-experimentation

Docs on running Airflow with Docker at: https://airflow.apache.org/docs/apache-airflow/stable/howto/docker-compose/index.html

We've removed Celery, Flower, and Redis from the compose file.

## Initializating Environment

init the config (optional)
```
docker compose run airflow-cli airflow config list
```

init the database
```
docker compose up airflow-init
```

to start airflow
```
docker compose up -d
```

to clean up the environment
```
docker compose down --volumes --remove-orphans
```