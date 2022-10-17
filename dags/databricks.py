"""
DAG that shows how to use the DatabricksSubmitRun and DatabricksRunNow operators.

Shows how to create a new cluster for the SubmitRun operator, as well as how to pass custom parameters to the RunNowOperator.
"""

from airflow import DAG
from airflow.providers.databricks.operators.databricks import (
    DatabricksSubmitRunOperator,
    DatabricksRunNowOperator,
)
from datetime import datetime, timedelta

# Define params for Submit Run Operator
new_cluster = {
    "spark_version": "7.3.x-scala2.12",
    "num_workers": 2,
    "node_type_id": "i3.xlarge",
}

notebook_task = {
    "notebook_path": "/Users/ExampleUser/Quickstart_Notebook",
}

# Define params for Run Now Operator
notebook_params = {"Variable": 5}


with DAG(
    "databricks_dag",
    start_date=datetime(2021, 1, 1),
    schedule_interval="@daily",
    catchup=False,
    default_args={
        "email_on_failure": False,
        "email_on_retry": False,
        "retries": 1,
        "retry_delay": timedelta(minutes=2),
    },
) as dag:

    opr_submit_run = DatabricksSubmitRunOperator(
        task_id="submit_run",
        databricks_conn_id="databricks",
        new_cluster=new_cluster,
        notebook_task=notebook_task,
    )

    opr_run_now = DatabricksRunNowOperator(
        task_id="run_now",
        databricks_conn_id="databricks",
        job_id=5,
        notebook_params=notebook_params,
    )

    opr_submit_run >> opr_run_now
