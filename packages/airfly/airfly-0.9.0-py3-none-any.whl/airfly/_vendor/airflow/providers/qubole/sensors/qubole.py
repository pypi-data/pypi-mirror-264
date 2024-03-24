# Auto generated by 'inv collect-airflow'
from airfly._vendor.airflow.sensors.base import BaseSensorOperator


class QuboleSensor(BaseSensorOperator):
    data: "_empty"
    qubole_conn_id: "str"


class QuboleFileSensor(QuboleSensor):
    pass


class QubolePartitionSensor(QuboleSensor):
    pass
