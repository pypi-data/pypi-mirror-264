# Auto generated by 'inv collect-airflow'
from airfly._vendor.airflow.sensors.base import BaseSensorOperator


class MongoSensor(BaseSensorOperator):
    collection: "str"
    query: "dict"
    mongo_conn_id: "str"
    mongo_db: "_empty"
