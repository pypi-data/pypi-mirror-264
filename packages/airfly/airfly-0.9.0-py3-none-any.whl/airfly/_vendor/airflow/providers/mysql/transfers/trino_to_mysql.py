# Auto generated by 'inv collect-airflow'
from airfly._vendor.airflow.models.baseoperator import BaseOperator


class TrinoToMySqlOperator(BaseOperator):
    sql: "str"
    mysql_table: "str"
    trino_conn_id: "str"
    mysql_conn_id: "str"
    mysql_preoperator: "str | None"
