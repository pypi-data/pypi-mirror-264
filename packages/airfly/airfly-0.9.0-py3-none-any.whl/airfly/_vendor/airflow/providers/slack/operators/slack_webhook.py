# Auto generated by 'inv collect-airflow'
from airfly._vendor.airflow.models.baseoperator import BaseOperator


class SlackWebhookOperator(BaseOperator):
    slack_webhook_conn_id: "_empty"
    message: "str"
    attachments: "list | None"
    blocks: "list | None"
    channel: "str | None"
    username: "str | None"
    icon_emoji: "str | None"
    icon_url: "str | None"
    proxy: "str | None"
    timeout: "int | None"
    retry_handlers: "list[RetryHandler] | None"
