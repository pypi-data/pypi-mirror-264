# Auto generated by 'inv collect-airflow'
from airfly._vendor.airflow.models.baseoperator import BaseOperator


class SalesforceApexRestOperator(BaseOperator):
    endpoint: "str"
    method: "str"
    payload: "dict"
    salesforce_conn_id: "str"
