# Auto generated by 'inv collect-airflow'
from airfly._vendor.airflow.providers.google.cloud.operators.cloud_base import (
    GoogleCloudBaseOperator,
)


class StackdriverListAlertPoliciesOperator(GoogleCloudBaseOperator):
    format_: "str | None"
    filter_: "str | None"
    order_by: "str | None"
    page_size: "int | None"
    retry: "Retry | _MethodDefault"
    timeout: "float | None"
    metadata: "Sequence[tuple[str, str]]"
    gcp_conn_id: "str"
    project_id: "str | None"
    impersonation_chain: "str | Sequence[str] | None"


class StackdriverEnableAlertPoliciesOperator(GoogleCloudBaseOperator):
    filter_: "str | None"
    retry: "Retry | _MethodDefault"
    timeout: "float | None"
    metadata: "Sequence[tuple[str, str]]"
    gcp_conn_id: "str"
    project_id: "str | None"
    impersonation_chain: "str | Sequence[str] | None"


class StackdriverDisableAlertPoliciesOperator(GoogleCloudBaseOperator):
    filter_: "str | None"
    retry: "Retry | _MethodDefault"
    timeout: "float | None"
    metadata: "Sequence[tuple[str, str]]"
    gcp_conn_id: "str"
    project_id: "str | None"
    impersonation_chain: "str | Sequence[str] | None"


class StackdriverUpsertAlertOperator(GoogleCloudBaseOperator):
    alerts: "str"
    retry: "Retry | _MethodDefault"
    timeout: "float | None"
    metadata: "Sequence[tuple[str, str]]"
    gcp_conn_id: "str"
    project_id: "str | None"
    impersonation_chain: "str | Sequence[str] | None"


class StackdriverDeleteAlertOperator(GoogleCloudBaseOperator):
    name: "str"
    retry: "Retry | _MethodDefault"
    timeout: "float | None"
    metadata: "Sequence[tuple[str, str]]"
    gcp_conn_id: "str"
    project_id: "str | None"
    impersonation_chain: "str | Sequence[str] | None"


class StackdriverListNotificationChannelsOperator(GoogleCloudBaseOperator):
    format_: "str | None"
    filter_: "str | None"
    order_by: "str | None"
    page_size: "int | None"
    retry: "Retry | _MethodDefault"
    timeout: "float | None"
    metadata: "Sequence[tuple[str, str]]"
    gcp_conn_id: "str"
    project_id: "str | None"
    impersonation_chain: "str | Sequence[str] | None"


class StackdriverEnableNotificationChannelsOperator(GoogleCloudBaseOperator):
    filter_: "str | None"
    retry: "Retry | _MethodDefault"
    timeout: "float | None"
    metadata: "Sequence[tuple[str, str]]"
    gcp_conn_id: "str"
    project_id: "str | None"
    impersonation_chain: "str | Sequence[str] | None"


class StackdriverDisableNotificationChannelsOperator(GoogleCloudBaseOperator):
    filter_: "str | None"
    retry: "Retry | _MethodDefault"
    timeout: "float | None"
    metadata: "Sequence[tuple[str, str]]"
    gcp_conn_id: "str"
    project_id: "str | None"
    impersonation_chain: "str | Sequence[str] | None"


class StackdriverUpsertNotificationChannelOperator(GoogleCloudBaseOperator):
    channels: "str"
    retry: "Retry | _MethodDefault"
    timeout: "float | None"
    metadata: "Sequence[tuple[str, str]]"
    gcp_conn_id: "str"
    project_id: "str | None"
    impersonation_chain: "str | Sequence[str] | None"


class StackdriverDeleteNotificationChannelOperator(GoogleCloudBaseOperator):
    name: "str"
    retry: "Retry | _MethodDefault"
    timeout: "float | None"
    metadata: "Sequence[tuple[str, str]]"
    gcp_conn_id: "str"
    project_id: "str | None"
    impersonation_chain: "str | Sequence[str] | None"
