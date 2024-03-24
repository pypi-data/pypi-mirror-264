# Auto generated by 'inv collect-airflow'
from airfly._vendor.airflow.models.baseoperator import BaseOperator


class EmrAddStepsOperator(BaseOperator):
    job_flow_id: "str | None"
    job_flow_name: "str | None"
    cluster_states: "list[str] | None"
    aws_conn_id: "str | None"
    steps: "list[dict] | str | None"
    wait_for_completion: "bool"
    waiter_delay: "int"
    waiter_max_attempts: "int"
    execution_role_arn: "str | None"
    deferrable: "bool"


class EmrStartNotebookExecutionOperator(BaseOperator):
    editor_id: "str"
    relative_path: "str"
    cluster_id: "str"
    service_role: "str"
    notebook_execution_name: "str | None"
    notebook_params: "str | None"
    notebook_instance_security_group_id: "str | None"
    master_instance_security_group_id: "str | None"
    tags: "list | None"
    wait_for_completion: "bool"
    aws_conn_id: "str | None"
    waiter_max_attempts: "int | None | ArgNotSet"
    waiter_delay: "int | None | ArgNotSet"
    waiter_countdown: "int"
    waiter_check_interval_seconds: "int"


class EmrStopNotebookExecutionOperator(BaseOperator):
    notebook_execution_id: "str"
    wait_for_completion: "bool"
    aws_conn_id: "str | None"
    waiter_max_attempts: "int | None | ArgNotSet"
    waiter_delay: "int | None | ArgNotSet"
    waiter_countdown: "int"
    waiter_check_interval_seconds: "int"


class EmrEksCreateClusterOperator(BaseOperator):
    virtual_cluster_name: "str"
    eks_cluster_name: "str"
    eks_namespace: "str"
    virtual_cluster_id: "str"
    aws_conn_id: "str | None"
    tags: "dict | None"


class EmrContainerOperator(BaseOperator):
    name: "str"
    virtual_cluster_id: "str"
    execution_role_arn: "str"
    release_label: "str"
    job_driver: "dict"
    configuration_overrides: "dict | None"
    client_request_token: "str | None"
    aws_conn_id: "str | None"
    wait_for_completion: "bool"
    poll_interval: "int"
    max_tries: "int | None"
    tags: "dict | None"
    max_polling_attempts: "int | None"
    job_retry_max_attempts: "int | None"
    deferrable: "bool"


class EmrCreateJobFlowOperator(BaseOperator):
    aws_conn_id: "str | None"
    emr_conn_id: "str | None"
    job_flow_overrides: "str | dict[str, Any] | None"
    region_name: "str | None"
    wait_for_completion: "bool"
    waiter_max_attempts: "int | None"
    waiter_delay: "int | None"
    waiter_countdown: "int | None"
    waiter_check_interval_seconds: "int"
    deferrable: "bool"


class EmrModifyClusterOperator(BaseOperator):
    cluster_id: "str"
    step_concurrency_level: "int"
    aws_conn_id: "str | None"


class EmrTerminateJobFlowOperator(BaseOperator):
    job_flow_id: "str"
    aws_conn_id: "str | None"
    waiter_delay: "int"
    waiter_max_attempts: "int"
    deferrable: "bool"


class EmrServerlessCreateApplicationOperator(BaseOperator):
    release_label: "str"
    job_type: "str"
    client_request_token: "str"
    config: "dict | None"
    wait_for_completion: "bool"
    aws_conn_id: "str | None"
    waiter_countdown: "int | ArgNotSet"
    waiter_check_interval_seconds: "int | ArgNotSet"
    waiter_max_attempts: "int | ArgNotSet"
    waiter_delay: "int | ArgNotSet"
    deferrable: "bool"


class EmrServerlessStartJobOperator(BaseOperator):
    application_id: "str"
    execution_role_arn: "str"
    job_driver: "dict"
    configuration_overrides: "dict | None"
    client_request_token: "str"
    config: "dict | None"
    wait_for_completion: "bool"
    aws_conn_id: "str | None"
    name: "str | None"
    waiter_countdown: "int | ArgNotSet"
    waiter_check_interval_seconds: "int | ArgNotSet"
    waiter_max_attempts: "int | ArgNotSet"
    waiter_delay: "int | ArgNotSet"
    deferrable: "bool"
    enable_application_ui_links: "bool"


class EmrServerlessStopApplicationOperator(BaseOperator):
    application_id: "str"
    wait_for_completion: "bool"
    aws_conn_id: "str | None"
    waiter_countdown: "int | ArgNotSet"
    waiter_check_interval_seconds: "int | ArgNotSet"
    waiter_max_attempts: "int | ArgNotSet"
    waiter_delay: "int | ArgNotSet"
    force_stop: "bool"
    deferrable: "bool"


class EmrServerlessDeleteApplicationOperator(EmrServerlessStopApplicationOperator):
    application_id: "str"
    wait_for_completion: "bool"
    aws_conn_id: "str | None"
    waiter_countdown: "int | ArgNotSet"
    waiter_check_interval_seconds: "int | ArgNotSet"
    waiter_max_attempts: "int | ArgNotSet"
    waiter_delay: "int | ArgNotSet"
    force_stop: "bool"
    deferrable: "bool"
