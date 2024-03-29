from pydantic import BaseModel, field_validator
from typing import Dict, List, TypedDict

from notdiamond.exceptions import MissingApiKey, InvalidApiKey


class NDApiKeyValidator(BaseModel):
    api_key: str

    @field_validator('api_key', mode='before')
    @classmethod
    def api_key_must_be_a_string(cls, v) -> str:
        if type(v) is not str:
            raise InvalidApiKey("ND API key should be a string")
        return v

    @field_validator('api_key', mode="after")
    @classmethod
    def string_must_not_be_empty(cls, v):
        if len(v) == 0:
            raise MissingApiKey("ND API key should be longer than 0")
        return v


class RequestProvider(TypedDict):
    provider: str
    model: str


class ModelSelectRequestPayload(BaseModel):
    prompt_template: str
    formatted_prompt: str
    components: Dict[str, Dict]
    llm_providers: List[Dict]
    metric: str
    max_model_depth: int


class FeedbackRequestPayload(BaseModel):
    session_id: str
    provider: RequestProvider
    feedback: Dict[str, int]
