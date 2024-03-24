# Auto generated by 'inv collect-airflow'
from airfly._vendor.airflow.models.baseoperator import BaseOperator
from airfly._vendor.airflow.providers.amazon.aws.utils.mixins import AwsBaseHookMixin


class AwsBaseOperator(BaseOperator, AwsBaseHookMixin):
    aws_conn_id: "str | None"
    region_name: "str | None"
    verify: "bool | str | None"
    botocore_config: "dict | None"
