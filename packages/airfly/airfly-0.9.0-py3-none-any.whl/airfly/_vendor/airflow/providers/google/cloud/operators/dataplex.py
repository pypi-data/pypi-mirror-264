# Auto generated by 'inv collect-airflow'
from airfly._vendor.airflow.providers.google.cloud.operators.cloud_base import (
    GoogleCloudBaseOperator,
)


class DataplexCreateTaskOperator(GoogleCloudBaseOperator):
    project_id: "str"
    region: "str"
    lake_id: "str"
    body: "dict[str, Any]"
    dataplex_task_id: "str"
    validate_only: "bool | None"
    api_version: "str"
    retry: "Retry | _MethodDefault"
    timeout: "float | None"
    metadata: "Sequence[tuple[str, str]]"
    gcp_conn_id: "str"
    impersonation_chain: "str | Sequence[str] | None"
    asynchronous: "bool"


class DataplexDeleteTaskOperator(GoogleCloudBaseOperator):
    project_id: "str"
    region: "str"
    lake_id: "str"
    dataplex_task_id: "str"
    api_version: "str"
    retry: "Retry | _MethodDefault"
    timeout: "float | None"
    metadata: "Sequence[tuple[str, str]]"
    gcp_conn_id: "str"
    impersonation_chain: "str | Sequence[str] | None"


class DataplexListTasksOperator(GoogleCloudBaseOperator):
    project_id: "str"
    region: "str"
    lake_id: "str"
    page_size: "int | None"
    page_token: "str | None"
    filter: "str | None"
    order_by: "str | None"
    api_version: "str"
    retry: "Retry | _MethodDefault"
    timeout: "float | None"
    metadata: "Sequence[tuple[str, str]]"
    gcp_conn_id: "str"
    impersonation_chain: "str | Sequence[str] | None"


class DataplexGetTaskOperator(GoogleCloudBaseOperator):
    project_id: "str"
    region: "str"
    lake_id: "str"
    dataplex_task_id: "str"
    api_version: "str"
    retry: "Retry | _MethodDefault"
    timeout: "float | None"
    metadata: "Sequence[tuple[str, str]]"
    gcp_conn_id: "str"
    impersonation_chain: "str | Sequence[str] | None"


class DataplexCreateLakeOperator(GoogleCloudBaseOperator):
    project_id: "str"
    region: "str"
    lake_id: "str"
    body: "dict[str, Any]"
    validate_only: "bool | None"
    api_version: "str"
    retry: "Retry | _MethodDefault"
    timeout: "float | None"
    metadata: "Sequence[tuple[str, str]]"
    gcp_conn_id: "str"
    impersonation_chain: "str | Sequence[str] | None"
    asynchronous: "bool"


class DataplexDeleteLakeOperator(GoogleCloudBaseOperator):
    project_id: "str"
    region: "str"
    lake_id: "str"
    api_version: "str"
    retry: "Retry | _MethodDefault"
    timeout: "float | None"
    metadata: "Sequence[tuple[str, str]]"
    gcp_conn_id: "str"
    impersonation_chain: "str | Sequence[str] | None"


class DataplexCreateOrUpdateDataQualityScanOperator(GoogleCloudBaseOperator):
    project_id: "str"
    region: "str"
    data_scan_id: "str"
    body: "dict[str, Any] | DataScan"
    api_version: "str"
    retry: "Retry | _MethodDefault"
    timeout: "float | None"
    update_mask: "dict | FieldMask | None"
    metadata: "Sequence[tuple[str, str]]"
    gcp_conn_id: "str"
    impersonation_chain: "str | Sequence[str] | None"


class DataplexGetDataQualityScanOperator(GoogleCloudBaseOperator):
    project_id: "str"
    region: "str"
    data_scan_id: "str"
    api_version: "str"
    retry: "Retry | _MethodDefault"
    timeout: "float | None"
    metadata: "Sequence[tuple[str, str]]"
    gcp_conn_id: "str"
    impersonation_chain: "str | Sequence[str] | None"


class DataplexDeleteDataQualityScanOperator(GoogleCloudBaseOperator):
    project_id: "str"
    region: "str"
    data_scan_id: "str"
    api_version: "str"
    retry: "Retry | _MethodDefault"
    timeout: "float | None"
    metadata: "Sequence[tuple[str, str]]"
    gcp_conn_id: "str"
    impersonation_chain: "str | Sequence[str] | None"


class DataplexRunDataQualityScanOperator(GoogleCloudBaseOperator):
    project_id: "str"
    region: "str"
    data_scan_id: "str"
    api_version: "str"
    retry: "Retry | _MethodDefault"
    timeout: "float | None"
    metadata: "Sequence[tuple[str, str]]"
    gcp_conn_id: "str"
    impersonation_chain: "str | Sequence[str] | None"
    asynchronous: "bool"
    fail_on_dq_failure: "bool"
    result_timeout: "float"
    deferrable: "bool"
    polling_interval_seconds: "int"


class DataplexGetDataQualityScanResultOperator(GoogleCloudBaseOperator):
    project_id: "str"
    region: "str"
    data_scan_id: "str"
    job_id: "str | None"
    api_version: "str"
    retry: "Retry | _MethodDefault"
    timeout: "float | None"
    metadata: "Sequence[tuple[str, str]]"
    gcp_conn_id: "str"
    impersonation_chain: "str | Sequence[str] | None"
    fail_on_dq_failure: "bool"
    wait_for_results: "bool"
    result_timeout: "float"
    deferrable: "bool"
    polling_interval_seconds: "int"


class DataplexCreateOrUpdateDataProfileScanOperator(GoogleCloudBaseOperator):
    project_id: "str"
    region: "str"
    data_scan_id: "str"
    body: "dict[str, Any] | DataScan"
    api_version: "str"
    retry: "Retry | _MethodDefault"
    timeout: "float | None"
    update_mask: "dict | FieldMask | None"
    metadata: "Sequence[tuple[str, str]]"
    gcp_conn_id: "str"
    impersonation_chain: "str | Sequence[str] | None"


class DataplexGetDataProfileScanOperator(GoogleCloudBaseOperator):
    project_id: "str"
    region: "str"
    data_scan_id: "str"
    api_version: "str"
    retry: "Retry | _MethodDefault"
    timeout: "float | None"
    metadata: "Sequence[tuple[str, str]]"
    gcp_conn_id: "str"
    impersonation_chain: "str | Sequence[str] | None"


class DataplexDeleteDataProfileScanOperator(GoogleCloudBaseOperator):
    project_id: "str"
    region: "str"
    data_scan_id: "str"
    api_version: "str"
    retry: "Retry | _MethodDefault"
    timeout: "float | None"
    metadata: "Sequence[tuple[str, str]]"
    gcp_conn_id: "str"
    impersonation_chain: "str | Sequence[str] | None"


class DataplexRunDataProfileScanOperator(GoogleCloudBaseOperator):
    project_id: "str"
    region: "str"
    data_scan_id: "str"
    api_version: "str"
    retry: "Retry | _MethodDefault"
    timeout: "float | None"
    metadata: "Sequence[tuple[str, str]]"
    gcp_conn_id: "str"
    impersonation_chain: "str | Sequence[str] | None"
    asynchronous: "bool"
    result_timeout: "float"
    deferrable: "bool"
    polling_interval_seconds: "int"


class DataplexGetDataProfileScanResultOperator(GoogleCloudBaseOperator):
    project_id: "str"
    region: "str"
    data_scan_id: "str"
    job_id: "str | None"
    api_version: "str"
    retry: "Retry | _MethodDefault"
    timeout: "float | None"
    metadata: "Sequence[tuple[str, str]]"
    gcp_conn_id: "str"
    impersonation_chain: "str | Sequence[str] | None"
    wait_for_results: "bool"
    result_timeout: "float"


class DataplexCreateZoneOperator(GoogleCloudBaseOperator):
    project_id: "str"
    region: "str"
    lake_id: "str"
    body: "dict[str, Any] | Zone"
    zone_id: "str"
    api_version: "str"
    retry: "Retry | _MethodDefault"
    timeout: "float | None"
    metadata: "Sequence[tuple[str, str]]"
    gcp_conn_id: "str"
    impersonation_chain: "str | Sequence[str] | None"


class DataplexDeleteZoneOperator(GoogleCloudBaseOperator):
    project_id: "str"
    region: "str"
    lake_id: "str"
    zone_id: "str"
    api_version: "str"
    retry: "Retry | _MethodDefault"
    timeout: "float | None"
    metadata: "Sequence[tuple[str, str]]"
    gcp_conn_id: "str"
    impersonation_chain: "str | Sequence[str] | None"


class DataplexCreateAssetOperator(GoogleCloudBaseOperator):
    project_id: "str"
    region: "str"
    lake_id: "str"
    body: "dict[str, Any] | Asset"
    zone_id: "str"
    asset_id: "str"
    api_version: "str"
    retry: "Retry | _MethodDefault"
    timeout: "float | None"
    metadata: "Sequence[tuple[str, str]]"
    gcp_conn_id: "str"
    impersonation_chain: "str | Sequence[str] | None"


class DataplexDeleteAssetOperator(GoogleCloudBaseOperator):
    project_id: "str"
    region: "str"
    lake_id: "str"
    zone_id: "str"
    asset_id: "str"
    api_version: "str"
    retry: "Retry | _MethodDefault"
    timeout: "float | None"
    metadata: "Sequence[tuple[str, str]]"
    gcp_conn_id: "str"
    impersonation_chain: "str | Sequence[str] | None"
