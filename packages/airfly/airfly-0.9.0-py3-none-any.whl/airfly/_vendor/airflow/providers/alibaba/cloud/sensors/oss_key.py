# Auto generated by 'inv collect-airflow'
from airfly._vendor.airflow.sensors.base import BaseSensorOperator


class OSSKeySensor(BaseSensorOperator):
    bucket_key: "str"
    region: "str"
    bucket_name: "str | None"
    oss_conn_id: "str | None"
