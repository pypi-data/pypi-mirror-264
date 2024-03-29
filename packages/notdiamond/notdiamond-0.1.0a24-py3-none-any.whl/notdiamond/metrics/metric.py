from typing import Optional

from notdiamond.types import NDApiKeyValidator
from notdiamond.metrics.request import feedback_request
from notdiamond.exceptions import ApiError
from notdiamond.llms.provider import NDLLMProvider


class NDMetric:
    def __init__(self, metric: Optional[str] = "accuracy"):
        self.metric = metric

    def __call__(self):
        return self.metric

    def feedback(self,
                 session_id: str,
                 llm_provider: NDLLMProvider,
                 value: int,
                 notdiamond_api_key: str):
        NDApiKeyValidator(api_key=notdiamond_api_key)
        if value not in [0, 1]:
            raise ApiError("Invalid feedback value. It must be 0 or 1.")

        return feedback_request(session_id=session_id,
                                llm_provider=llm_provider,
                                feedback_payload=self.request_payload(value),
                                notdiamond_api_key=notdiamond_api_key)
    
    def request_payload(self, value: int):
        return { self.metric: value }
