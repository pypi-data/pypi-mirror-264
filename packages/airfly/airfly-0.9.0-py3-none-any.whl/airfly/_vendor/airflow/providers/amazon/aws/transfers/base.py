# Auto generated by 'inv collect-airflow'
from airfly._vendor.airflow.models.baseoperator import BaseOperator


class AwsToAwsBaseOperator(BaseOperator):
    source_aws_conn_id: "str | None"
    dest_aws_conn_id: "str | None | ArgNotSet"
    aws_conn_id: "str | None | ArgNotSet"
