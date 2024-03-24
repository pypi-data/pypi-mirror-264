# Auto generated by 'inv collect-airflow'
from airfly._vendor.airflow.models.baseoperator import BaseOperator


class ImapAttachmentToS3Operator(BaseOperator):
    imap_attachment_name: "str"
    s3_bucket: "str"
    s3_key: "str"
    imap_check_regex: "bool"
    imap_mail_folder: "str"
    imap_mail_filter: "str"
    s3_overwrite: "bool"
    imap_conn_id: "str"
    aws_conn_id: "str | None"
