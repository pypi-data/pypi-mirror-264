# Auto generated by 'inv collect-airflow'
from airfly._vendor.airflow.models.baseoperator import BaseOperator


class SqlToS3Operator(BaseOperator):
    query: "str"
    s3_bucket: "str"
    s3_key: "str"
    sql_conn_id: "str"
    sql_hook_params: "dict | None"
    parameters: "None | Mapping[str, Any] | list | tuple"
    replace: "bool"
    aws_conn_id: "str | None"
    verify: "bool | str | None"
    file_format: "Literal['csv', 'json', 'parquet']"
    max_rows_per_file: "int"
    pd_kwargs: "dict | None"
    groupby_kwargs: "dict | None"
