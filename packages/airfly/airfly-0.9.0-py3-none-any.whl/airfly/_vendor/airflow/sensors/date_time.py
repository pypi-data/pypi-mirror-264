# Auto generated by 'inv collect-airflow'
from airfly._vendor.airflow.sensors.base import BaseSensorOperator


class DateTimeSensor(BaseSensorOperator):
    target_time: "typing.Union[str, datetime.datetime]"
