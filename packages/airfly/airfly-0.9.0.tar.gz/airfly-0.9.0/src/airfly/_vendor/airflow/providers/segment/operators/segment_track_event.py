# Auto generated by 'inv collect-airflow'
from airfly._vendor.airflow.models.baseoperator import BaseOperator


class SegmentTrackEventOperator(BaseOperator):
    user_id: "str"
    event: "str"
    properties: "dict | None"
    segment_conn_id: "str"
    segment_debug_mode: "bool"
