# Auto generated by 'inv collect-airflow'
from airfly._vendor.airflow.providers.slack.transfers.base_sql_to_slack import (
    BaseSqlToSlackOperator,
)


class SqlToSlackWebhookOperator(BaseSqlToSlackOperator):
    sql: "str"
    sql_conn_id: "str"
    slack_webhook_conn_id: "str | None"
    sql_hook_params: "dict | None"
    slack_channel: "str | None"
    slack_message: "str"
    results_df_name: "str"
    parameters: "list | tuple | Mapping[str, Any] | None"
