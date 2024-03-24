# Auto generated by 'inv collect-airflow'
from airfly._vendor.airflow.providers.amazon.aws.transfers.base import (
    AwsToAwsBaseOperator,
)


class DynamoDBToS3Operator(AwsToAwsBaseOperator):
    dynamodb_table_name: "str"
    s3_bucket_name: "str"
    file_size: "int"
    dynamodb_scan_kwargs: "dict[str, Any] | None"
    s3_key_prefix: "str"
    process_func: "Callable[[dict[str, Any]], bytes]"
    export_time: "datetime | None"
    export_format: "str"
    check_interval: "int"
    max_attempts: "int"
