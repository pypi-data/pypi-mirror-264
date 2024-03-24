# Auto generated by 'inv collect-airflow'
from airfly._vendor.airflow.providers.google.cloud.operators.cloud_base import (
    GoogleCloudBaseOperator,
)


class RunPipelineJobOperator(GoogleCloudBaseOperator):
    project_id: "str"
    region: "str"
    display_name: "str"
    template_path: "str"
    job_id: "str | None"
    pipeline_root: "str | None"
    parameter_values: "dict[str, Any] | None"
    input_artifacts: "dict[str, str] | None"
    enable_caching: "bool | None"
    encryption_spec_key_name: "str | None"
    labels: "dict[str, str] | None"
    failure_policy: "str | None"
    service_account: "str | None"
    network: "str | None"
    create_request_timeout: "float | None"
    experiment: "str | experiment_resources.Experiment | None"
    gcp_conn_id: "str"
    impersonation_chain: "str | Sequence[str] | None"


class GetPipelineJobOperator(GoogleCloudBaseOperator):
    project_id: "str"
    region: "str"
    pipeline_job_id: "str"
    retry: "Retry | _MethodDefault"
    timeout: "float | None"
    metadata: "Sequence[tuple[str, str]]"
    gcp_conn_id: "str"
    impersonation_chain: "str | Sequence[str] | None"


class ListPipelineJobOperator(GoogleCloudBaseOperator):
    region: "str"
    project_id: "str"
    page_size: "int | None"
    page_token: "str | None"
    filter: "str | None"
    order_by: "str | None"
    retry: "Retry | _MethodDefault"
    timeout: "float | None"
    metadata: "Sequence[tuple[str, str]]"
    gcp_conn_id: "str"
    impersonation_chain: "str | Sequence[str] | None"


class DeletePipelineJobOperator(GoogleCloudBaseOperator):
    project_id: "str"
    region: "str"
    pipeline_job_id: "str"
    retry: "Retry | _MethodDefault"
    timeout: "float | None"
    metadata: "Sequence[tuple[str, str]]"
    gcp_conn_id: "str"
    impersonation_chain: "str | Sequence[str] | None"
