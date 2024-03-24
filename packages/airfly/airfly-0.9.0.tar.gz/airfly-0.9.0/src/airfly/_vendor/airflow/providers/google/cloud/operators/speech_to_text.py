# Auto generated by 'inv collect-airflow'
from airfly._vendor.airflow.providers.google.cloud.operators.cloud_base import (
    GoogleCloudBaseOperator,
)


class CloudSpeechToTextRecognizeSpeechOperator(GoogleCloudBaseOperator):
    audio: "RecognitionAudio"
    config: "RecognitionConfig"
    project_id: "str | None"
    gcp_conn_id: "str"
    retry: "Retry | _MethodDefault"
    timeout: "float | None"
    impersonation_chain: "str | Sequence[str] | None"
