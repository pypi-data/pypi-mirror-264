# Auto generated by 'inv collect-airflow'
from airfly._vendor.airflow.sensors.base import BaseSensorOperator


class TaskQueueEmptySensor(BaseSensorOperator):
    location: "str"
    project_id: "str | None"
    queue_name: "str | None"
    gcp_conn_id: "str"
    impersonation_chain: "str | Sequence[str] | None"
