# Auto generated by 'inv collect-airflow'
from airfly._vendor.airflow.models.baseoperator import BaseOperator


class TriggerDagRunOperator(BaseOperator):
    trigger_dag_id: "str"
    trigger_run_id: "str | None"
    conf: "dict | None"
    execution_date: "str | datetime.datetime | None"
    reset_dag_run: "bool"
    wait_for_completion: "bool"
    poke_interval: "int"
    allowed_states: "list[str] | None"
    failed_states: "list[str] | None"
    deferrable: "bool"
