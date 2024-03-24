# Auto generated by 'inv collect-airflow'
from airfly._vendor.airflow.providers.amazon.aws.operators.base_aws import (
    AwsBaseOperator,
)


class DataSyncOperator(AwsBaseOperator):
    wait_interval_seconds: "int"
    max_iterations: "int"
    wait_for_completion: "bool"
    task_arn: "str | None"
    source_location_uri: "str | None"
    destination_location_uri: "str | None"
    allow_random_task_choice: "bool"
    allow_random_location_choice: "bool"
    create_task_kwargs: "dict | None"
    create_source_location_kwargs: "dict | None"
    create_destination_location_kwargs: "dict | None"
    update_task_kwargs: "dict | None"
    task_execution_kwargs: "dict | None"
    delete_task_after_execution: "bool"
