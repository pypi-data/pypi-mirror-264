# Auto generated by 'inv collect-airflow'
from airfly._vendor.airflow.providers.slack.transfers.base_sql_to_slack import (
    BaseSqlToSlackOperator,
)
from airfly._vendor.airflow.providers.slack.transfers.sql_to_slack_webhook import (
    SqlToSlackWebhookOperator,
)


class SqlToSlackApiFileOperator(BaseSqlToSlackOperator):
    sql: "str"
    sql_conn_id: "str"
    sql_hook_params: "dict | None"
    parameters: "list | tuple | Mapping[str, Any] | None"
    slack_conn_id: "str"
    slack_filename: "str"
    slack_channels: "str | Sequence[str] | None"
    slack_initial_comment: "str | None"
    slack_title: "str | None"
    slack_base_url: "str | None"
    slack_method_version: "Literal['v1', 'v2']"
    df_kwargs: "dict | None"


class SqlToSlackOperator(SqlToSlackWebhookOperator):
    pass
