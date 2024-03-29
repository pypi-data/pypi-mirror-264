import random
import requests

from notdiamond import settings
from notdiamond.prompts.prompt import NDPromptTemplate, NDChatPromptTemplate
from notdiamond.prompts.hash import nd_hash
from notdiamond.metrics.metric import NDMetric
from notdiamond.llms.provider import NDLLMProvider
from notdiamond.exceptions import ApiError
from notdiamond.types import ModelSelectRequestPayload

from typing import List, Optional, Union, Dict
import json


def model_select(prompt_template: Optional[Union[NDPromptTemplate, NDChatPromptTemplate]],
                 llm_providers: List[NDLLMProvider],
                 metric: NDMetric,
                 notdiamond_api_key: str,
                 max_model_depth: int,
                 preference_weights: Optional[Dict[str, float]] = None,
                 preference_id: Optional[str] = None):
    """NotDiamond model select based on prompt
    """

    url = f"{settings.ND_BASE_URL}/v1/optimizer/modelSelect"

    payload: ModelSelectRequestPayload = {
        "prompt_template": prompt_template.template,
        "formatted_prompt": nd_hash(prompt_template.format()),
        "components": prompt_template.prepare_for_request(),
        "llm_providers": [llm_provider.prepare_for_request() for llm_provider in llm_providers],
        "metric": metric.metric,
        "max_model_depth": max_model_depth,
    }

    if preference_weights is not None:
        payload['preference_weights'] = preference_weights
    if preference_id is not None:
        payload['preference_id'] = preference_id

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {notdiamond_api_key}"
    }

    try:
        response = requests.post(url, data=json.dumps(payload), headers=headers)
    except Exception as e:
        raise ApiError(f"ND API error for modelSelect: {e}")

    if response.status_code == 200:
        response_json = response.json()

        providers = response_json['providers']
        session_id = response_json['session_id']

        # TODO: make use of full providers list in the future and rest of params returned
        top_provider = providers[0]

        best_llm = list(filter(lambda x: (x.model == top_provider['model']) & (x.provider == top_provider['provider']),
                               llm_providers))[0]
        return best_llm, session_id
    else:
        print(f"ND API error: {response.status_code}")
        return None, 'NO-SESSION-ID'


def report_latency(session_id: str,
                   llm_provider: NDLLMProvider,
                   tokens_per_second: float,
                   notdiamond_api_key: str):
    """NotDiamond API to report latency of LLM call
    """
    url = f"{settings.ND_BASE_URL}/v1/report/metrics/latency"

    payload = {
        "session_id": session_id,
        "provider": llm_provider.prepare_for_request(),
        "latency": {"tokens_per_second": tokens_per_second}
    }

    headers = {
        "content-type": "application/json",
        "Authorization": f"Bearer {notdiamond_api_key}"
    }

    try:
        response = requests.post(url, json=payload, headers=headers)
    except Exception as e:
        raise ApiError(f"ND API error for report metrics latency: {e}")

    return response.status_code
