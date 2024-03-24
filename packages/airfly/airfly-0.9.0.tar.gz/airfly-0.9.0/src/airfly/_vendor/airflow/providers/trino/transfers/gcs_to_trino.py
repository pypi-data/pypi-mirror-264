# Auto generated by 'inv collect-airflow'
from airfly._vendor.airflow.models.baseoperator import BaseOperator


class GCSToTrinoOperator(BaseOperator):
    source_bucket: "str"
    source_object: "str"
    trino_table: "str"
    trino_conn_id: "str"
    gcp_conn_id: "str"
    schema_fields: "Iterable[str] | None"
    schema_object: "str | None"
    impersonation_chain: "str | Sequence[str] | None"
