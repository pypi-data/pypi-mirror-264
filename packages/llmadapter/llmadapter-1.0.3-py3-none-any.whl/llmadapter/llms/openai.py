"""Wrapper around OpenAI APIs."""
from __future__ import annotations

import logging
import sys
import warnings
import openai
from typing import (
    AbstractSet,
    Any,
    Callable,
    Collection,
    Dict,
    Generator,
    List,
    Literal,
    Mapping,
    Optional,
    Set,
    Tuple,
    Union,
    AsyncGenerator,
)

from pydantic import Field, root_validator
from tenacity import (
    before_sleep_log,
    retry,
    retry_if_exception_type,
    stop_after_attempt,
    wait_exponential,
)

from llmadapter.callbacks.manager import (
    AsyncCallbackManagerForLLMRun,
    CallbackManagerForLLMRun,
)
from llmadapter.llms.base import BaseLLM
from llmadapter.schema import (
    Generation,
    LLMResult,
    BaseMessage,
    ChatResult,
    ChatGeneration,
    ChatMessage,
    HumanMessage,
    AIMessage,
    SystemMessage,
    FunctionMessage
)
from llmadapter.utils import get_from_dict_or_env

logger = logging.getLogger(__name__)


def update_token_usage(
    keys: Set[str], response: Dict[str, Any], token_usage: Dict[str, Any]
) -> None:
    """Update token usage."""
    _keys_to_use = keys.intersection(response["usage"])
    for _key in _keys_to_use:
        if _key not in token_usage:
            token_usage[_key] = response["usage"][_key]
        else:
            token_usage[_key] += response["usage"][_key]


def _update_response(response: Dict[str, Any], stream_response: Dict[str, Any]) -> None:
    """Update response from the stream response."""
    response["choices"][0]["text"] += stream_response["choices"][0]["text"]
    response["choices"][0]["finish_reason"] = stream_response["choices"][0][
        "finish_reason"
    ]
    response["choices"][0]["logprobs"] = stream_response["choices"][0]["logprobs"]


def _streaming_response_template() -> Dict[str, Any]:
    return {
        "choices": [
            {
                "text": "",
                "finish_reason": None,
                "logprobs": None,
            }
        ]
    }

def _convert_dict_to_message(_dict: Mapping[str, Any]) -> BaseMessage:
    role = _dict["role"]
    if role == "user":
        return HumanMessage(content=_dict["content"])
    elif role == "assistant":
        content = _dict["content"] or ""  # OpenAI returns None for tool invocations
        if _dict.get("function_call"):
            additional_kwargs = {"function_call": dict(_dict["function_call"])}
        else:
            additional_kwargs = {}
        return AIMessage(content=content, additional_kwargs=additional_kwargs)
    elif role == "system":
        return SystemMessage(content=_dict["content"])
    else:
        return ChatMessage(content=_dict["content"], role=role)


def _convert_message_to_dict(message: BaseMessage) -> dict:
    if isinstance(message, ChatMessage):
        message_dict = {"role": message.role, "content": message.content}
    elif isinstance(message, HumanMessage):
        message_dict = {"role": "user", "content": message.content}
    elif isinstance(message, AIMessage):
        message_dict = {"role": "assistant", "content": message.content}
        if "function_call" in message.additional_kwargs:
            message_dict["function_call"] = message.additional_kwargs["function_call"]
    elif isinstance(message, SystemMessage):
        message_dict = {"role": "system", "content": message.content}
    elif isinstance(message, FunctionMessage):
        message_dict = {
            "role": "function",
            "content": message.content,
            "name": message.name,
        }
    else:
        raise ValueError(f"Got unknown type {message}")
    if "name" in message.additional_kwargs:
        message_dict["name"] = message.additional_kwargs["name"]
    return message_dict

def _create_retry_decorator(llm: BaseOpenAI) -> Callable[[Any], Any]:
    import openai

    min_seconds = 4
    max_seconds = 10
    # Wait 2^x * 1 second between each retry starting with
    # 4 seconds, then up to 10 seconds, then 10 seconds afterwards
    return retry(
        reraise=True,
        stop=stop_after_attempt(llm.max_retries),
        wait=wait_exponential(multiplier=1, min=min_seconds, max=max_seconds),
        retry=(
            retry_if_exception_type(openai.error.Timeout)
            | retry_if_exception_type(openai.error.APIError)
            | retry_if_exception_type(openai.error.APIConnectionError)
            | retry_if_exception_type(openai.error.RateLimitError)
            | retry_if_exception_type(openai.error.ServiceUnavailableError)
        ),
        before_sleep=before_sleep_log(logger, logging.WARNING),
    )

def fastchat_tokenizer_decode(base_url: str, model_name: str, token_ids: List[int]) -> str:
    import requests
    import json
    response = requests.post(
        url=f"{base_url}/tokenizer/decode",
        json={
            "model": model_name,
            "token_ids": token_ids
        },
        verify=False,
        timeout=30,
    )
    if response.status_code != 200:
        raise ValueError(
            f"tokenizer_decode call failed with status code {response.status_code}."
            f" Details: {json.dumps(response.json())}"
        )
    return response.json()["text"]

def fastchat_tokenizer_encode(base_url: str, model_name: str, text: str) -> List[int]:
    import requests
    import json
    response = requests.post(
        url=f"{base_url}/tokenizer/encode",
        json={
            "model": model_name,
            "text": text
        },
        verify=False,
        timeout=30,
    )
    if response.status_code != 200:
        raise ValueError(
            f"tokenizer_encode call failed with status code {response.status_code}."
            f" Details: {json.dumps(response.json())}"
        )
    return response.json()["token_ids"]

def completion_with_retry(llm: BaseOpenAI, openai_client: Any, **kwargs: Any) -> Any:
    """Use tenacity to retry the completion call."""
    retry_decorator = _create_retry_decorator(llm)

    @retry_decorator
    def _completion_with_retry(**kwargs: Any) -> Any:
        return openai_client.create(**kwargs)

    return _completion_with_retry(**kwargs)


async def acompletion_with_retry(llm: BaseOpenAI, openai_client: Any, **kwargs: Any) -> Any:
    """Use tenacity to retry the async completion call."""
    retry_decorator = _create_retry_decorator(llm)

    @retry_decorator
    async def _completion_with_retry(**kwargs: Any) -> Any:
        # Use OpenAI's async api https://github.com/openai/openai-python#async-api
        return await openai_client.acreate(**kwargs)

    return await _completion_with_retry(**kwargs)


class BaseOpenAI(BaseLLM):
    """Wrapper around OpenAI large language models."""

    @property
    def lc_secrets(self) -> Dict[str, str]:
        return {"openai_api_key": "OPENAI_API_KEY"}

    @property
    def lc_serializable(self) -> bool:
        return True

    model_name: str = Field("text-davinci-003", alias="model")
    """Model name to use."""
    temperature: float = 0.7
    """What sampling temperature to use."""
    max_tokens: int = 256
    """The maximum number of tokens to generate in the completion.
    -1 returns as many tokens as possible given the prompt and
    the models maximal context size."""
    top_p: float = 1
    """Total probability mass of tokens to consider at each step."""
    frequency_penalty: float = 0
    """Penalizes repeated tokens according to frequency."""
    presence_penalty: float = 0
    """Penalizes repeated tokens."""
    n: int = 1
    """How many completions to generate for each prompt."""
    best_of: int = 1
    """Generates best_of completions server-side and returns the "best"."""
    model_kwargs: Dict[str, Any] = Field(default_factory=dict)
    """Holds any model parameters valid for `create` call not explicitly specified."""
    openai_api_key: Optional[str] = None
    openai_api_base: Optional[str] = None
    openai_organization: Optional[str] = None
    # to support explicit proxy for OpenAI
    openai_proxy: Optional[str] = None
    batch_size: int = 20
    """Batch size to use when passing multiple documents to generate."""
    request_timeout: Optional[Union[float, Tuple[float, float]]] = None
    """Timeout for requests to OpenAI completion API. Default is 600 seconds."""
    logit_bias: Optional[Dict[str, float]] = Field(default_factory=dict)
    """Adjust the probability of specific tokens being generated."""
    max_retries: int = 6
    """Maximum number of retries to make when generating."""
    streaming: bool = False
    """Whether to stream the results or not."""
    allowed_special: Union[Literal["all"], AbstractSet[str]] = set()
    """Set of special tokens that are allowed。"""
    disallowed_special: Union[Literal["all"], Collection[str]] = "all"
    """Set of special tokens that are not allowed。"""

    class Config:
        """Configuration for this pydantic object."""

        allow_population_by_field_name = True

    @root_validator(pre=True)
    def build_extra(cls, values: Dict[str, Any]) -> Dict[str, Any]:
        """Build extra kwargs from additional params that were passed in."""
        all_required_field_names = cls.all_required_field_names()
        extra = values.get("model_kwargs", {})
        for field_name in list(values):
            if field_name in extra:
                raise ValueError(f"Found {field_name} supplied twice.")
            if field_name not in all_required_field_names:
                extra[field_name] = values.pop(field_name)

        invalid_model_kwargs = all_required_field_names.intersection(extra.keys())
        if invalid_model_kwargs:
            raise ValueError(
                f"Parameters {invalid_model_kwargs} should be specified explicitly. "
                f"Instead they were passed in as part of `model_kwargs` parameter."
            )

        values["model_kwargs"] = extra
        return values

    @root_validator()
    def validate_environment(cls, values: Dict) -> Dict:
        """Validate that api key and python package exists in environment."""
        values["openai_api_key"] = get_from_dict_or_env(
            values, "openai_api_key", "OPENAI_API_KEY", "Empty"
        )
        values["openai_api_base"] = get_from_dict_or_env(
            values,
            "openai_api_base",
            "OPENAI_API_BASE",
            default="",
        )
        values["openai_proxy"] = get_from_dict_or_env(
            values,
            "openai_proxy",
            "OPENAI_PROXY",
            default="",
        )
        values["openai_organization"] = get_from_dict_or_env(
            values,
            "openai_organization",
            "OPENAI_ORGANIZATION",
            default="",
        )
        if values["streaming"] and values["n"] > 1:
            raise ValueError("Cannot stream results when n > 1.")
        if values["streaming"] and values["best_of"] > 1:
            raise ValueError("Cannot stream results when best_of > 1.")
        return values

    @property
    def _default_params(self) -> Dict[str, Any]:
        """Get the default parameters for calling OpenAI API."""
        normal_params = {
            "temperature": self.temperature,
            "max_tokens": self.max_tokens,
            "top_p": self.top_p,
            "frequency_penalty": self.frequency_penalty,
            "presence_penalty": self.presence_penalty,
            "n": self.n,
            "request_timeout": self.request_timeout,
            "logit_bias": self.logit_bias,
        }

        # Azure gpt-35-turbo doesn't support best_of
        # don't specify best_of if it is 1
        if self.best_of > 1:
            normal_params["best_of"] = self.best_of

        return {**normal_params, **self.model_kwargs}

    def _generate_prompt(
        self,
        prompts: List[str],
        stop: Optional[List[str]] = None,
        run_manager: Optional[CallbackManagerForLLMRun] = None,
        **kwargs: Any,
    ) -> LLMResult:
        """Call out to OpenAI's endpoint with k unique prompts.

        Args:
            prompts: The prompts to pass into the model.
            stop: Optional list of stop words to use when generating.

        Returns:
            The full LLM output.

        Example:
            .. code-block:: python

                response = openai.generate(["Tell me a joke."])
        """
        # TODO: write a unit test for this
        params = self._invocation_params
        params = {**params, **kwargs}
        sub_prompts = self.get_sub_prompts(params, prompts, stop)
        choices = []
        token_usage: Dict[str, int] = {}
        # Get the token usage from the response.
        # Includes prompt, completion, and total tokens used.
        _keys = {"completion_tokens", "prompt_tokens", "total_tokens"}
        for _prompts in sub_prompts:
            if self.streaming:
                if len(_prompts) > 1:
                    raise ValueError("Cannot stream results with multiple prompts.")
                params["stream"] = True
                response = _streaming_response_template()
                for stream_resp in completion_with_retry(
                    self, openai_client=openai.Completion, prompt=_prompts, **params
                ):
                    if run_manager:
                        run_manager.on_llm_new_token(
                            stream_resp["choices"][0]["text"],
                            verbose=self.verbose,
                            logprobs=stream_resp["choices"][0]["logprobs"],
                        )
                    _update_response(response, stream_resp)
                choices.extend(response["choices"])
            else:
                response = completion_with_retry(self, openai_client=openai.Completion, prompt=_prompts, **params)
                choices.extend(response["choices"])
            if not self.streaming:
                # Can't update token usage if streaming
                update_token_usage(_keys, response, token_usage)
        return self.create_llm_result(choices, prompts, token_usage)

    async def _agenerate_prompt(
        self,
        prompts: List[str],
        stop: Optional[List[str]] = None,
        run_manager: Optional[AsyncCallbackManagerForLLMRun] = None,
        **kwargs: Any,
    ) -> LLMResult:
        """Call out to OpenAI's endpoint async with k unique prompts."""
        params = self._invocation_params
        params = {**params, **kwargs}
        sub_prompts = self.get_sub_prompts(params, prompts, stop)
        choices = []
        token_usage: Dict[str, int] = {}
        # Get the token usage from the response.
        # Includes prompt, completion, and total tokens used.
        _keys = {"completion_tokens", "prompt_tokens", "total_tokens"}
        for _prompts in sub_prompts:
            if self.streaming:
                if len(_prompts) > 1:
                    raise ValueError("Cannot stream results with multiple prompts.")
                params["stream"] = True
                response = _streaming_response_template()
                async for stream_resp in await acompletion_with_retry(
                    self, openai_client=openai.Completion, prompt=_prompts, **params
                ):
                    if run_manager:
                        await run_manager.on_llm_new_token(
                            stream_resp["choices"][0]["text"],
                            verbose=self.verbose,
                            logprobs=stream_resp["choices"][0]["logprobs"],
                        )
                    _update_response(response, stream_resp)
                choices.extend(response["choices"])
            else:
                response = await acompletion_with_retry(self, openai_client=openai.Completion, prompt=_prompts, **params)
                choices.extend(response["choices"])
            if not self.streaming:
                # Can't update token usage if streaming
                update_token_usage(_keys, response, token_usage)
        return self.create_llm_result(choices, prompts, token_usage)

    def get_sub_prompts(
        self,
        params: Dict[str, Any],
        prompts: List[str],
        stop: Optional[List[str]] = None,
    ) -> List[List[str]]:
        """Get the sub prompts for llm call."""
        if stop is not None:
            if "stop" in params:
                raise ValueError("`stop` found in both the input and default params.")
            params["stop"] = stop
        if params["max_tokens"] == -1:
            if len(prompts) != 1:
                raise ValueError(
                    "max_tokens set to -1 not supported for multiple inputs."
                )
            params["max_tokens"] = self.max_tokens_for_prompt(prompts[0])
        sub_prompts = [
            prompts[i : i + self.batch_size]
            for i in range(0, len(prompts), self.batch_size)
        ]
        return sub_prompts

    def create_llm_result(
        self, choices: Any, prompts: List[str], token_usage: Dict[str, int]
    ) -> LLMResult:
        """Create the LLMResult from the choices and prompts."""
        generations = []
        for i, _ in enumerate(prompts):
            sub_choices = choices[i * self.n : (i + 1) * self.n]
            generations.append(
                [
                    Generation(
                        text=choice["text"],
                        generation_info=dict(
                            finish_reason=choice.get("finish_reason"),
                            logprobs=choice.get("logprobs"),
                        ),
                    )
                    for choice in sub_choices
                ]
            )
        llm_output = {"token_usage": token_usage, "model_name": self.model_name}
        return LLMResult(generations=generations, llm_output=llm_output)

    def stream_generator(self, prompt: Union[List[BaseMessage], str], stop: Optional[List[str]] = None, **kwargs: Any) -> Generator:
        """Call OpenAI with streaming flag and return the resulting generator.

        BETA: this is a beta feature while we figure out the right abstraction.
        Once that happens, this interface could change.

        Args:
            prompt: The prompts to pass into the model.
            stop: Optional list of stop words to use when generating.

        Returns:
            A generator representing the stream of tokens from OpenAI.

        Example:
            .. code-block:: python

                generator = openai.stream("Tell me a joke.")
                for token in generator:
                    yield token
        """
        import openai
        params = self.prep_streaming_params(stop)
        params = {**params, **kwargs}
        if isinstance(prompt, str):
            generator = completion_with_retry(self, openai_client=openai.Completion, prompt=prompt, **params)
            for tokens_info in generator:
                tokens = tokens_info["choices"][0]["text"]
                yield tokens
        elif all(isinstance(message, BaseMessage) for message in prompt):
            messages = [_convert_message_to_dict(m) for m in prompt]
            generator = completion_with_retry(self, openai_client=openai.ChatCompletion, messages=messages, **params)
            for tokens_info in generator:
                tokens = tokens_info["choices"][0]["delta"].get("content") or ""
                yield tokens
        else:
            raise ValueError(
                "Argument 'prompt' is expected to be of type List[BaseMessage] or str, received"
                f" argument of type {type(prompt)}."
            )

    async def astream_generator(self, prompt: Union[List[BaseMessage], str], stop: Optional[List[str]] = None, **kwargs: Any) -> AsyncGenerator:
        """Call OpenAI with streaming flag and return the resulting generator.

        BETA: this is a beta feature while we figure out the right abstraction.
        Once that happens, this interface could change.

        Args:
            prompt: The prompts to pass into the model.
            stop: Optional list of stop words to use when generating.

        Returns:
            A generator representing the stream of tokens from OpenAI.

        Example:
            .. code-block:: python

                generator = openai.stream("Tell me a joke.")
                async for token in generator:
                    yield token
        """
        import openai
        params = self.prep_streaming_params(stop)
        params = {**params, **kwargs}
        if isinstance(prompt, str):
            generator = await acompletion_with_retry(self, openai_client=openai.Completion, prompt=prompt, **params)
            async for tokens_info in generator:
                tokens = tokens_info["choices"][0]["text"]
                yield tokens
        elif all(isinstance(message, BaseMessage) for message in prompt):
            messages = [_convert_message_to_dict(m) for m in prompt]
            generator = await acompletion_with_retry(self, openai_client=openai.ChatCompletion, messages=messages, **params)
            async for tokens_info in generator:
                tokens = tokens_info["choices"][0]["delta"].get("content") or ""
                yield tokens
        else:
            raise ValueError(
                "Argument 'prompt' is expected to be of type List[BaseMessage] or str, received"
                f" argument of type {type(prompt)}."
            )

    def prep_streaming_params(self, stop: Optional[List[str]] = None) -> Dict[str, Any]:
        """Prepare the params for streaming."""
        params = self._invocation_params
        if "best_of" in params and params["best_of"] != 1:
            raise ValueError("OpenAI only supports best_of == 1 for streaming")
        if stop is not None:
            if "stop" in params:
                raise ValueError("`stop` found in both the input and default params.")
            params["stop"] = stop
        params["stream"] = True
        return params

    def _generate_messages(
        self,
        messages: List[BaseMessage],
        stop: Optional[List[str]] = None,
        run_manager: Optional[CallbackManagerForLLMRun] = None,
        **kwargs: Any,
    ) -> ChatResult:
        message_dicts, params = self._create_message_dicts(messages, stop)
        params = {**params, **kwargs}
        if self.streaming:
            inner_completion = ""
            role = "assistant"
            params["stream"] = True
            function_call: Optional[dict] = None
            for stream_resp in completion_with_retry(
                self, openai_client=openai.ChatCompletion, messages=message_dicts, **params
            ):
                role = stream_resp["choices"][0]["delta"].get("role", role)
                token = stream_resp["choices"][0]["delta"].get("content") or ""
                inner_completion += token
                _function_call = stream_resp["choices"][0]["delta"].get("function_call")
                if _function_call:
                    if function_call is None:
                        function_call = _function_call
                    else:
                        function_call["arguments"] += _function_call["arguments"]
                if run_manager:
                    run_manager.on_llm_new_token(token)
            message = _convert_dict_to_message(
                {
                    "content": inner_completion,
                    "role": role,
                    "function_call": function_call,
                }
            )
            return ChatResult(generations=[ChatGeneration(message=message)])
        response = completion_with_retry(self, openai_client=openai.ChatCompletion, messages=message_dicts, **params)
        return self._create_chat_result(response)

    def _create_message_dicts(
        self, messages: List[BaseMessage], stop: Optional[List[str]]
    ) -> Tuple[List[Dict[str, Any]], Dict[str, Any]]:
        params = dict(self._invocation_params)
        if stop is not None:
            if "stop" in params:
                raise ValueError("`stop` found in both the input and default params.")
            params["stop"] = stop
        message_dicts = [_convert_message_to_dict(m) for m in messages]
        return message_dicts, params

    def _create_chat_result(self, response: Mapping[str, Any]) -> ChatResult:
        generations = []
        for res in response["choices"]:
            message = _convert_dict_to_message(res["message"])
            gen = ChatGeneration(message=message)
            generations.append(gen)
        llm_output = {"token_usage": response["usage"], "model_name": self.model_name}
        return ChatResult(generations=generations, llm_output=llm_output)

    def _combine_llm_outputs(self, llm_outputs: List[Optional[dict]]) -> dict:
        overall_token_usage: dict = {}
        for output in llm_outputs:
            if output is None:
                # Happens in streaming
                continue
            token_usage = output["token_usage"]
            for k, v in token_usage.items():
                if k in overall_token_usage:
                    overall_token_usage[k] += v
                else:
                    overall_token_usage[k] = v
        return {"token_usage": overall_token_usage, "model_name": self.model_name}

    async def _agenerate_messages(
        self,
        messages: List[BaseMessage],
        stop: Optional[List[str]] = None,
        run_manager: Optional[AsyncCallbackManagerForLLMRun] = None,
        **kwargs: Any,
    ) -> ChatResult:
        message_dicts, params = self._create_message_dicts(messages, stop)
        params = {**params, **kwargs}
        if self.streaming:
            inner_completion = ""
            role = "assistant"
            params["stream"] = True
            function_call: Optional[dict] = None
            async for stream_resp in await acompletion_with_retry(
                self, openai_client=openai.ChatCompletion, messages=message_dicts, **params
            ):
                role = stream_resp["choices"][0]["delta"].get("role", role)
                token = stream_resp["choices"][0]["delta"].get("content", "")
                inner_completion += token or ""
                _function_call = stream_resp["choices"][0]["delta"].get("function_call")
                if _function_call:
                    if function_call is None:
                        function_call = _function_call
                    else:
                        function_call["arguments"] += _function_call["arguments"]
                if run_manager:
                    await run_manager.on_llm_new_token(token)
            message = _convert_dict_to_message(
                {
                    "content": inner_completion,
                    "role": role,
                    "function_call": function_call,
                }
            )
            return ChatResult(generations=[ChatGeneration(message=message)])
        else:
            response = await acompletion_with_retry(
                self, openai_client=openai.ChatCompletion, messages=message_dicts, **params
            )
            return self._create_chat_result(response)

    @property
    def _invocation_params(self) -> Dict[str, Any]:
        """Get the parameters used to invoke the model."""
        openai_creds: Dict[str, Any] = {
            "api_key": self.openai_api_key,
            "api_base": self.openai_api_base,
            "organization": self.openai_organization,
        }
        if self.openai_proxy:
            import openai

            openai.proxy = {"http": self.openai_proxy, "https": self.openai_proxy}  # type: ignore[assignment]  # noqa: E501
        return {**openai_creds, **self._default_params}

    @property
    def _identifying_params(self) -> Mapping[str, Any]:
        """Get the identifying parameters."""
        return {**{"model_name": self.model_name}, **self._default_params}

    @property
    def _llm_type(self) -> str:
        """Return type of llm."""
        return "openai"

    def tokenizer_encode(self, text: str) -> List[int]:
        """Get the token IDs using the tiktoken package."""
        # tiktoken NOT supported for Python < 3.8
        if sys.version_info[1] < 8:
            return super().get_num_tokens(text)
        try:
            import tiktoken
            from tiktoken.model import MODEL_TO_ENCODING
        except ImportError:
            raise ImportError(
                "Could not import tiktoken python package. "
                "This is needed in order to calculate get_num_tokens. "
                "Please install it with `pip install tiktoken`."
            )

        token_ids = []
        if self.model_name in MODEL_TO_ENCODING:
            enc = tiktoken.encoding_for_model(self.model_name)
            token_ids = enc.encode(
                text,
                allowed_special=self.allowed_special,
                disallowed_special=self.disallowed_special,
            )
        else:
            token_ids = fastchat_tokenizer_encode(self.openai_api_base, self.model_name, text)
        return token_ids

    def tokenizer_decode(self, tokens: List[int]) -> str:
        """Get the text present in the tokens."""
        # tiktoken NOT supported for Python < 3.8
        if sys.version_info[1] < 8:
            raise ValueError("tiktoken NOT supported for Python < 3.8")
        try:
            import tiktoken
            from tiktoken.model import MODEL_TO_ENCODING
        except ImportError:
            raise ImportError(
                "Could not import tiktoken python package. "
                "This is needed in order to calculate get_num_tokens. "
                "Please install it with `pip install tiktoken`."
            )

        text = ""
        if self.model_name in MODEL_TO_ENCODING:
            enc = tiktoken.encoding_for_model(self.model_name)
            text = enc.decode(
                tokens
            )
        else:
            text = fastchat_tokenizer_decode(self.openai_api_base, self.model_name, tokens)
        return text

    def get_context_size(self) -> int:
        """Get the llm max tokens."""
        model_token_mapping = {
            "gpt-4": 8192,
            "gpt-4-0314": 8192,
            "gpt-4-32k": 32768,
            "gpt-4-32k-0314": 32768,
            "gpt-3.5-turbo": 4096,
            "gpt-3.5-turbo-0301": 4096,
            "text-ada-001": 2049,
            "ada": 2049,
            "text-babbage-001": 2040,
            "babbage": 2049,
            "text-curie-001": 2049,
            "curie": 2049,
            "davinci": 2049,
            "text-davinci-003": 4097,
            "text-davinci-002": 4097,
            "code-davinci-002": 8001,
            "code-davinci-001": 8001,
            "code-cushman-002": 2048,
            "code-cushman-001": 2048,
        }

        context_size = model_token_mapping.get(self.model_name, None)

        # 为None时调FastChat接口获取
        if context_size is None:
            import requests
            import json
            response = requests.get(
                url=f"{self.openai_api_base}/{self.model_name}/config",
                verify=False,
                timeout=30,
            )
            if response.status_code != 200:
                raise ValueError(
                    f"fastchat call failed with status code {response.status_code}."
                    f" Details: {json.dumps(response.json())}"
                )
            context_size = response.json()["max_tokens_length"]

        return context_size

    def get_fastchat_conversation_length(self) -> Dict:
        """Get the conversation_length"""
        import requests
        import json
        response = requests.get(
            url=f"{self.openai_api_base}/{self.model_name}/conversation_length",
            verify=False,
            timeout=30,
        )
        if response.status_code != 200:
            raise ValueError(
                f"fastchat call failed with status code {response.status_code}."
                f" Details: {json.dumps(response.json())}"
            )
        conversation = {
            "tokens_without_system_role": response.json()["tokens_without_system_role"],
            "tokens_init_system_role": response.json()["tokens_init_system_role"]
        }

        return conversation

    @staticmethod
    def modelname_to_contextsize(modelname: str) -> int:
        """Calculate the maximum number of tokens possible to generate for a model.

        Args:
            modelname: The modelname we want to know the context size for.

        Returns:
            The maximum context size

        Example:
            .. code-block:: python

                max_tokens = openai.modelname_to_contextsize("text-davinci-003")
        """
        model_token_mapping = {
            "gpt-4": 8192,
            "gpt-4-0314": 8192,
            "gpt-4-32k": 32768,
            "gpt-4-32k-0314": 32768,
            "gpt-3.5-turbo": 4096,
            "gpt-3.5-turbo-0301": 4096,
            "text-ada-001": 2049,
            "ada": 2049,
            "text-babbage-001": 2040,
            "babbage": 2049,
            "text-curie-001": 2049,
            "curie": 2049,
            "davinci": 2049,
            "text-davinci-003": 4097,
            "text-davinci-002": 4097,
            "code-davinci-002": 8001,
            "code-davinci-001": 8001,
            "code-cushman-002": 2048,
            "code-cushman-001": 2048,
        }

        # handling finetuned models
        if "ft-" in modelname:
            modelname = modelname.split(":")[0]

        context_size = model_token_mapping.get(modelname, None)

        if context_size is None:
            raise ValueError(
                f"Unknown model: {modelname}. Please provide a valid OpenAI model name."
                "Known models are: " + ", ".join(model_token_mapping.keys())
            )

        return context_size

    @property
    def max_context_size(self) -> int:
        """Get max context size for this model."""
        return self.modelname_to_contextsize(self.model_name)

    def max_tokens_for_prompt(self, prompt: str) -> int:
        """Calculate the maximum number of tokens possible to generate for a prompt.

        Args:
            prompt: The prompt to pass into the model.

        Returns:
            The maximum number of tokens to generate for a prompt.

        Example:
            .. code-block:: python

                max_tokens = openai.max_token_for_prompt("Tell me a joke.")
        """
        num_tokens = self.get_num_tokens(prompt)
        return self.max_context_size - num_tokens


class OpenAI(BaseOpenAI):
    """Wrapper around OpenAI large language models.

    To use, you should have the ``openai`` python package installed, and the
    environment variable ``OPENAI_API_KEY`` set with your API key.

    Any parameters that are valid to be passed to the openai.create call can be passed
    in, even if not explicitly saved on this class.

    Example:
        .. code-block:: python

            from llmadapter.llms import OpenAI
            openai = OpenAI(model_name="text-davinci-003")
    """

    @property
    def _invocation_params(self) -> Dict[str, Any]:
        return {**{"model": self.model_name}, **super()._invocation_params}