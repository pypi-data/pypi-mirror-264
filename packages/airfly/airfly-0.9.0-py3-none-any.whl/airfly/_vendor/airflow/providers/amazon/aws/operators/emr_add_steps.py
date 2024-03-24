# Auto generated by 'inv collect-airflow'
from airfly._vendor.airflow.models.baseoperator import BaseOperator


class EmrAddStepsOperator(BaseOperator):
    job_flow_id: "typing.Union[str, NoneType]"
    job_flow_name: "typing.Union[str, NoneType]"
    cluster_states: "typing.Union[typing.List[str], NoneType]"
    aws_conn_id: "str"
    steps: "typing.Union[typing.List[dict], str, NoneType]"
