# Auto generated by 'inv collect-airflow'
from airfly._vendor.airflow.models.baseoperator import BaseOperator


class S3ToSFTPOperator(BaseOperator):
    s3_bucket: "str"
    s3_key: "str"
    sftp_path: "str"
    sftp_conn_id: "str"
    aws_conn_id: "str | None"
