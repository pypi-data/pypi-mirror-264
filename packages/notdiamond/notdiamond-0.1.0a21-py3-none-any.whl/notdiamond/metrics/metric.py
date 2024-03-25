from typing import Optional

from notdiamond.types import NDApiKeyValidator
from notdiamond.metrics.request import feedback_request


class NDMetric:
    def __init__(self, metric: Optional[str] = "accuracy"):
        self.metric = metric

    def __call__(self):
        return self.metric

    def feedback(self,
                 feedback_payload: dict,
                 session_id: str,
                 notdiamond_api_key: str):
        NDApiKeyValidator(api_key=notdiamond_api_key)

        response = feedback_request(feedback_payload, session_id, notdiamond_api_key)

        return response
