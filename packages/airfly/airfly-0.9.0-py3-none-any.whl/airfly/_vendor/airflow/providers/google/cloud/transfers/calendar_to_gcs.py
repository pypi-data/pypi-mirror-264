# Auto generated by 'inv collect-airflow'
from airfly._vendor.airflow.models.baseoperator import BaseOperator


class GoogleCalendarToGCSOperator(BaseOperator):
    destination_bucket: "str"
    api_version: "str"
    calendar_id: "str"
    i_cal_uid: "str | None"
    max_attendees: "int | None"
    max_results: "int | None"
    order_by: "str | None"
    private_extended_property: "str | None"
    text_search_query: "str | None"
    shared_extended_property: "str | None"
    show_deleted: "bool | None"
    show_hidden_invitation: "bool | None"
    single_events: "bool | None"
    sync_token: "str | None"
    time_max: "datetime | None"
    time_min: "datetime | None"
    time_zone: "str | None"
    updated_min: "datetime | None"
    destination_path: "str | None"
    gcp_conn_id: "str"
    impersonation_chain: "str | Sequence[str] | None"
