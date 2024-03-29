import time
from typing import Any, List, Dict, Optional, Union, Iterator

from langchain_core.messages import BaseMessageChunk, BaseMessage, AIMessage
from litellm import token_counter
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.callbacks.manager import CallbackManagerForLLMRun
from langchain_core.language_models.llms import LLM
from langchain.prompts import PromptTemplate
from langchain_anthropic import ChatAnthropic
from langchain_openai import ChatOpenAI
from langchain_community.chat_models.cohere import ChatCohere
from langchain_mistralai.chat_models import ChatMistralAI
from langchain_together import Together
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_google_genai.chat_models import ChatGoogleGenerativeAIError

from notdiamond import settings
from notdiamond.exceptions import ApiError, MissingLLMProviders
from notdiamond.llms.provider import NDLLMProvider
from notdiamond.prompts.prompt import NDPromptTemplate, NDChatPromptTemplate
from notdiamond.metrics.metric import NDMetric
from notdiamond.llms.request import model_select, report_latency
from notdiamond.types import NDApiKeyValidator


class NDLLM(LLM):
    """
    Custom implementation of NDLLM
    Starting reference is from here: https://python.langchain.com/docs/modules/model_io/llms/custom_llm
    """
    llm_providers: List[NDLLMProvider]
    api_key: str
    latency_tracking: bool = True
    default: Union[int, str] = None
    max_model_depth: int = None
    preference_weights: Optional[Dict[str, float]] = None
    preference_id: Optional[str] = None

    def __init__(self, **kwargs):
        kwargs['api_key'] = kwargs['api_key'] if kwargs.get('api_key') else settings.NOTDIAMOND_API_KEY
        NDApiKeyValidator(api_key=kwargs.get('api_key', ''))

        if len(kwargs.get('llm_providers', [])) == 0:
            raise MissingLLMProviders("No LLM provider was specified. Make sure there's at least one given.")
        kwargs['llm_providers'] = self._parse_llm_providers_data(kwargs.get('llm_providers', []))

        kwargs['max_model_depth'] = kwargs['max_model_depth'] if kwargs.get('max_model_depth') else len(kwargs['llm_providers'])
        if kwargs['max_model_depth'] == 0:
            raise ValueError("max_model_depth has to be bigger than 0.")

        if kwargs['max_model_depth'] > len(kwargs['llm_providers']):
            print("WARNING: max_model_depth cannot be bigger than the number of LLM providers.")
            kwargs['max_model_depth'] = len(kwargs['llm_providers'])
        
        if kwargs.get('preference_weights') is not None:
            for k, v in kwargs['preference_weights'].items():
                if k not in ['cost', 'quality', 'latency']:
                    raise ValueError("Invalid preference weights. Accepted keys are quality, cost and latency.")
                if v < 0 or v > 1:
                    raise ValueError("Invalid preference weights. Value must be between 0 and 1.")

        super(NDLLM, self).__init__(**kwargs)

    @property
    def default_llm_provider(self) -> Union[NDLLMProvider, None]:
        if self.default == None:
            return None
        else:
            if isinstance(self.default, int):
                return self.llm_providers[self.default]
            elif isinstance(self.default, str):
                return NDLLMProvider.from_string(self.default)
        return None

    @staticmethod
    def _parse_llm_providers_data(llm_providers: list) -> List[NDLLMProvider]:
        providers = []
        for llm_provider in llm_providers:
            if isinstance(llm_provider, NDLLMProvider):
                providers.append(llm_provider)
                continue
            parsed_provider = NDLLMProvider.from_string(llm_provider)
            providers.append(parsed_provider)
        return providers

    @property
    def _llm_type(self) -> str:
        return "NotDiamond LLM"

    def _call(self, prompt: str, stop: Optional[List[str]] = None,
              run_manager: Optional[CallbackManagerForLLMRun] = None, **kwargs: Any, ) -> str:
        if stop is not None:
            raise ValueError("stop kwargs are not permitted.")
        return "This function is deprecated for the latest LangChain version, use invoke instead"

    def invoke(self,
               prompt_template: Optional[Union[NDPromptTemplate, PromptTemplate,
                                               NDChatPromptTemplate, ChatPromptTemplate, str]],
               input: Optional[Dict[str, Any]] = {},
               metric: NDMetric = NDMetric("accuracy"), **kwargs) -> Any:
        if not isinstance(prompt_template, NDPromptTemplate) or not isinstance(prompt_template, NDChatPromptTemplate):
            prompt_template = self._prepare_prompt_template(prompt_template)
        
        prompt_template.partial_variables = {**prompt_template.partial_variables, **input}
        
        best_llm, session_id = model_select(prompt_template=prompt_template,
                                             llm_providers=self.llm_providers,
                                             metric=metric,
                                             notdiamond_api_key=self.api_key,
                                             max_model_depth=self.max_model_depth,
                                             preference_weights=self.preference_weights,
                                             preference_id=self.preference_id)
        
        is_default = False
        if not best_llm:
            best_llm = self.default_llm_provider
            is_default = True

            if best_llm == None:
                raise ApiError("ND couldn't find a suitable model to call. To avoid disruptions, we recommend setting a default fallback model or make max depth larger.")
        
        llm = self._llm_from_provider(best_llm)
        chain = prompt_template | llm

        try:
            if self.latency_tracking:
                result = self._invoke_with_latency_tracking(session_id=session_id,
                                                            chain=chain,
                                                            llm_provider=best_llm,
                                                            is_default=is_default,
                                                            input=input, **kwargs)
            else:
                result = chain.invoke(input, **kwargs)
        except (ChatGoogleGenerativeAIError, ValueError) as e:
            if isinstance(prompt_template, NDChatPromptTemplate) and best_llm.provider == 'google':
                print(f"WARNING: Google model's chat messages are violating requirements with error {e}.")
                print("If you see this message, means the NotDiamond API returned a Google model as the best option, but the LLM call will fail. So we will automatically fall back to a non-Google model, if possible.")

                non_google_llm = next(
                    (llm_provider for llm_provider in self.llm_providers if llm_provider.provider != 'google'),
                    None
                )

                if non_google_llm != None:
                    best_llm = non_google_llm
                    llm = self._llm_from_provider(best_llm)
                    chain = prompt_template | llm

                    if self.latency_tracking:
                        result = self._invoke_with_latency_tracking(session_id=session_id,
                                                                    chain=chain,
                                                                    llm_provider=best_llm,
                                                                    is_default=is_default,
                                                                    input=input,
                                                                    **kwargs)
                    else:
                        result = chain.invoke(input, **kwargs)
                else:
                    raise e
            else:
                raise e

        if isinstance(result, str):
            result = AIMessage(content=result)

        return result, session_id, best_llm

    def stream(self, input=None, **kwargs) -> Iterator[BaseMessageChunk]:
        """
        Stream the response from the LLM. A generator is returned. The generator yields chunks of the response.
        This is a wrapper around the `stream` method of an llm that returns a generator instead of the full response.
        """
        prompt_template = self._prepare_prompt_template(prompt_template=input)
        best_llm, session_id = model_select(prompt_template=prompt_template,
                                            llm_providers=self.llm_providers,
                                            metric=NDMetric("accuracy"),
                                            notdiamond_api_key=self.api_key,
                                            max_model_depth=self.max_model_depth,
                                            preference_weights=self.preference_weights,
                                            preference_id=self.preference_id)
        if not best_llm:
            best_llm = self.default_llm_provider

            if best_llm == None:
                raise ApiError("ND couldn't find a suitable model to call. To avoid disruptions, we recommend setting a default fallback model or make max depth larger.")

        llm = self._llm_from_provider(best_llm)
        for chunk in llm.stream(input, **kwargs):
            yield chunk
    
    def openai_model_select(self,
                            prompt_template: Optional[Union[NDPromptTemplate, NDChatPromptTemplate]],
                            metric: NDMetric = NDMetric("accuracy")):
        if not isinstance(prompt_template, NDPromptTemplate) or not isinstance(prompt_template, NDChatPromptTemplate):
            prompt_template = self._prepare_prompt_template(prompt_template)
        
        best_llm, _ = model_select(prompt_template=prompt_template,
                                   llm_providers=self.llm_providers,
                                   metric=metric,
                                   notdiamond_api_key=self.api_key,
                                   max_model_depth=self.max_model_depth,
                                   preference_weights=self.preference_weights,
                                   preference_id=self.preference_id)
        if not best_llm:
            best_llm = self.default_llm_provider

            if best_llm == None:
                raise ApiError("ND couldn't find a suitable model to call. To avoid disruptions, we recommend setting a default fallback model or make max depth larger.")

        return best_llm.model
    
    def model_select(self,
                     prompt_template: Optional[Union[NDPromptTemplate, PromptTemplate,
                                                     NDChatPromptTemplate, ChatPromptTemplate, str]],
                     input: Optional[Dict[str, Any]] = {},
                     metric: NDMetric = NDMetric("accuracy"), **kwargs: Any) -> Any:
        if not isinstance(prompt_template, NDPromptTemplate) or not isinstance(prompt_template, NDChatPromptTemplate):
            prompt_template = self._prepare_prompt_template(prompt_template)
        
        prompt_template.partial_variables = {**prompt_template.partial_variables, **input}
        
        best_llm, session_id = model_select(prompt_template=prompt_template,
                                            llm_providers=self.llm_providers,
                                            metric=metric,
                                            notdiamond_api_key=self.api_key,
                                            max_model_depth=self.max_model_depth,
                                            preference_weights=self.preference_weights,
                                            preference_id=self.preference_id)
        
        if not best_llm and self.default is not None:
            print("ND API error. Falling back to default provider.")
            best_llm = self.default_llm_provider

        return session_id, best_llm

    def _invoke_with_latency_tracking(self, session_id: str, chain: Any, llm_provider: NDLLMProvider,
                                      input: Optional[Dict[str, Any]] = {},
                                      is_default: Optional[bool] = True,
                                      **kwargs):
        if (session_id == "NO-SESSION-ID" or session_id == "") and not is_default:
            raise ApiError("ND session_id is not valid for latency tracking. Please check the API response.")

        start_time = time.time()
        result = chain.invoke(input, **kwargs)
        end_time = time.time()

        if isinstance(result, str):
            result = AIMessage(content=result)

        tokens_completed = token_counter(model=llm_provider.model, messages=[{"role": "assistant", "content": result.content}])
        tokens_per_second = tokens_completed / (end_time - start_time)

        report_latency(session_id=session_id,
                       llm_provider=llm_provider,
                       tokens_per_second=tokens_per_second,
                       notdiamond_api_key=self.api_key)

        return result

    @staticmethod
    def _llm_from_provider(provider: NDLLMProvider) -> Any:
        if provider.provider == 'openai':
            return ChatOpenAI(openai_api_key=provider.api_key,
                              model_name=provider.model,
                              **provider.kwargs)
        elif provider.provider == 'anthropic':
            return ChatAnthropic(anthropic_api_key=provider.api_key,
                                 model=provider.model,
                                 **provider.kwargs)
        elif provider.provider == 'google':
            return ChatGoogleGenerativeAI(google_api_key=provider.api_key,
                                          model=provider.model,
                                          convert_system_message_to_human=True,
                                          **provider.kwargs)
        elif provider.provider == 'cohere':
            return ChatCohere(cohere_api_key=provider.api_key,
                              model=provider.model,
                              **provider.kwargs)
        elif provider.provider == 'mistral':
            return ChatMistralAI(mistral_api_key=provider.api_key,
                                 model=provider.model,
                                 **provider.kwargs)
        elif provider.provider == 'togetherai':
            provider_settings = settings.PROVIDERS.get(provider.provider, None)
            model_prefixes = provider_settings.get('model_prefix', None)
            model_prefix = model_prefixes.get(provider.model, None)

            model = provider.model
            if model_prefix is not None:
                model = f"{model_prefix}/{provider.model}"
            print(f"MODEL: {model}")
            return Together(together_api_key=provider.api_key,
                            model=model,
                            **provider.kwargs)
        else:
            raise ValueError(f"Unsupported provider: {provider.provider}")

    @staticmethod
    def _prepare_prompt_template(prompt_template) -> Union[NDPromptTemplate, NDChatPromptTemplate]:
        if isinstance(prompt_template, str):
            return NDPromptTemplate(template=prompt_template)
        elif isinstance(prompt_template, PromptTemplate):
            return NDPromptTemplate.from_langchain_prompt_template(prompt_template)
        elif isinstance(prompt_template, NDPromptTemplate):
            return prompt_template
        elif isinstance(prompt_template, NDChatPromptTemplate):
            return prompt_template
        elif isinstance(prompt_template, ChatPromptTemplate):
            return NDChatPromptTemplate.from_langchain_chat_prompt_template(prompt_template)
        elif isinstance(prompt_template, list):
            if all(isinstance(pt, BaseMessage) for pt in prompt_template):
                return NDChatPromptTemplate.from_messages(prompt_template)
            else:
                raise ValueError(f"Unsupported prompt_template type {type(prompt_template)}")
        else:
            raise ValueError(f"Unsupported prompt_template type {type(prompt_template)}")
