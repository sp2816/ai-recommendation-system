from airflow import DAG
from airflow.providers.standard.operators.python import PythonOperator

from datetime import datetime


# ==========================
# TASK FUNCTIONS
# ==========================

def retrain_model():

    print(
        "Running weekly model retraining..."
    )


def update_embeddings():

    print(
        "Updating item embeddings..."
    )


def refresh_redis():

    print(
        "Refreshing Redis feature store..."
    )


# ==========================
# DAG CONFIG
# ==========================

default_args = {

    "owner":
        "selin",

    "start_date":
        datetime(
            2025,
            1,
            1
        )
}


dag = DAG(

    "recommendation_pipeline",

    default_args=default_args,

    schedule="@daily",

    catchup=False
)


# ==========================
# TASKS
# ==========================

retrain_task = PythonOperator(

    task_id=
    "weekly_model_retraining",

    python_callable=
    retrain_model,

    dag=dag
)


embedding_task = PythonOperator(

    task_id=
    "daily_embedding_update",

    python_callable=
    update_embeddings,

    dag=dag
)


redis_task = PythonOperator(

    task_id=
    "refresh_redis_store",

    python_callable=
    refresh_redis,

    dag=dag
)


# ==========================
# TASK FLOW
# ==========================

retrain_task >> embedding_task >> redis_task