"""Base interface for large language models to expose."""
import asyncio
import inspect
import json
import warnings
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any, Dict, List, Mapping, Optional, Tuple, Union, Generator, AsyncGenerator

import yaml
from pydantic import Field, root_validator, validator

import llmadapter
from llmadapter.base_language import BaseLanguageModel
from llmadapter.callbacks.base import BaseCallbackManager
from llmadapter.callbacks.manager import (
    AsyncCallbackManager,
    AsyncCallbackManagerForLLMRun,
    CallbackManager,
    CallbackManagerForLLMRun,
    Callbacks,
)
from llmadapter.load.dump import dumpd
from llmadapter.schema import (
    AIMessage,
    BaseMessage,
    Generation,
    LLMResult,
    RunInfo,
    ChatGeneration,
    ChatResult,
    get_buffer_string
)


def _get_verbosity() -> bool:
    return llmadapter.verbose

def chat_history_as_string(messages: List[BaseMessage]) -> str:
    return "\n".join([f"{m.type}: {m.content}" for m in messages])

def get_prompts(
    params: Dict[str, Any], prompts: List[str]
) -> Tuple[Dict[int, List], str, List[int], List[str]]:
    """Get prompts that are already cached."""
    llm_string = str(sorted([(k, v) for k, v in params.items()]))
    missing_prompts = []
    missing_prompt_idxs = []
    existing_prompts = {}
    for i, prompt in enumerate(prompts):
        if llmadapter.llm_cache is not None:
            cache_val = llmadapter.llm_cache.lookup(prompt, llm_string)
            if isinstance(cache_val, list):
                existing_prompts[i] = cache_val
            else:
                missing_prompts.append(prompt)
                missing_prompt_idxs.append(i)
    return existing_prompts, llm_string, missing_prompt_idxs, missing_prompts

def get_chat_prompts(
    params: Dict[str, Any], prompts: List[List[BaseMessage]]
) -> Tuple[Dict[int, ChatResult], str, List[int], List[List[BaseMessage]]]:
    """Get prompts that are already cached."""
    llm_string = str(sorted([(k, v) for k, v in params.items()]))
    missing_prompts = []
    missing_prompt_idxs = []
    existing_prompts = {}
    for i, prompt in enumerate(prompts):
        if llmadapter.llm_cache is not None:
            cache_val = llmadapter.llm_cache.lookup(
                chat_history_as_string(prompt), llm_string
            )
            if isinstance(cache_val, list):
                for i in range(len(cache_val)):
                    if "message" not in cache_val[i]:
                        message = AIMessage(content=cache_val[i].text)
                        chatGeneration = ChatGeneration(message=message)
                        cache_val[i] = chatGeneration

                existing_prompts[i] = ChatResult(generations=cache_val)
            else:
                missing_prompts.append(prompt)
                missing_prompt_idxs.append(i)
    return existing_prompts, llm_string, missing_prompt_idxs, missing_prompts

def update_cache(
    existing_prompts: Dict[int, List],
    llm_string: str,
    missing_prompt_idxs: List[int],
    new_results: LLMResult,
    prompts: List[str],
) -> Optional[dict]:
    """Update the cache and get the LLM output."""
    for i, result in enumerate(new_results.generations):
        existing_prompts[missing_prompt_idxs[i]] = result
        prompt = prompts[missing_prompt_idxs[i]]
        if llmadapter.llm_cache is not None:
            llmadapter.llm_cache.update(prompt, llm_string, result)
    llm_output = new_results.llm_output
    return llm_output

def update_chat_cache(
    existing_prompts: Dict[int, ChatResult],
    llm_string: str,
    missing_prompt_idxs: List[int],
    new_results: List[ChatResult],
    prompts: List[List[BaseMessage]],
) ->List[Optional[dict]]:
    """Update the cache and get the LLM output."""
    for i, result in enumerate(new_results):
        existing_prompts[missing_prompt_idxs[i]] = result
        prompt = prompts[missing_prompt_idxs[i]]
        if llmadapter.llm_cache is not None:
            llmadapter.llm_cache.update(chat_history_as_string(prompt), llm_string, result.generations)
    llm_output = [results.llm_output for results in new_results]
    return llm_output

def isListBaseMessage(info) -> bool:
    return all(isinstance(message, BaseMessage) for message in info)

class BaseLLM(BaseLanguageModel, ABC):
    """LLM wrapper should take in a prompt and return a string."""

    cache: Optional[bool] = None
    verbose: bool = Field(default_factory=_get_verbosity)
    """Whether to print out response text."""
    callbacks: Callbacks = Field(default=None, exclude=True)
    callback_manager: Optional[BaseCallbackManager] = Field(default=None, exclude=True)
    tags: Optional[List[str]] = Field(default=None, exclude=True)
    """Tags to add to the run trace."""

    class Config:
        """Configuration for this pydantic object."""

        arbitrary_types_allowed = True

    @root_validator()
    def raise_deprecation(cls, values: Dict) -> Dict:
        """Raise deprecation warning if callback_manager is used."""
        if values.get("callback_manager") is not None:
            warnings.warn(
                "callback_manager is deprecated. Please use callbacks instead.",
                DeprecationWarning,
            )
            values["callbacks"] = values.pop("callback_manager", None)
        return values

    @validator("verbose", pre=True, always=True)
    def set_verbose(cls, verbose: Optional[bool]) -> bool:
        """If verbose is None, set it.

        This allows users to pass in None as verbose to access the global setting.
        """
        if verbose is None:
            return _get_verbosity()
        else:
            return verbose

    @abstractmethod
    def stream_generator(
        self,
        prompt: Union[List[BaseMessage], str],
        stop: Optional[List[str]] = None,
        **kwargs: Any,
    ) -> Generator:
        """Run the LLM on the given prompts."""

    @abstractmethod
    async def astream_generator(
        self,
        prompt: Union[List[BaseMessage], str],
        stop: Optional[List[str]] = None,
        **kwargs: Any,
    ) -> AsyncGenerator:
        """Run the LLM on the given prompts."""

    @abstractmethod
    def _generate_prompt(
        self,
        prompts: List[str],
        stop: Optional[List[str]] = None,
        run_manager: Optional[CallbackManagerForLLMRun] = None,
        **kwargs: Any,
    ) -> LLMResult:
        """Run the LLM on the given prompts."""

    @abstractmethod
    async def _agenerate_prompt(
        self,
        prompts: List[str],
        stop: Optional[List[str]] = None,
        run_manager: Optional[AsyncCallbackManagerForLLMRun] = None,
        **kwargs: Any,
    ) -> LLMResult:
        """Run the LLM on the given prompts."""

    @abstractmethod
    def _generate_messages(
        self,
        messages: List[BaseMessage],
        stop: Optional[List[str]] = None,
        run_manager: Optional[CallbackManagerForLLMRun] = None,
        **kwargs: Any,
    ) -> ChatResult:
        """Run the LLM on the given messages."""

    @abstractmethod
    async def _agenerate_messages(
        self,
        messages: List[BaseMessage],
        stop: Optional[List[str]] = None,
        run_manager: Optional[AsyncCallbackManagerForLLMRun] = None,
        **kwargs: Any,
    ) -> ChatResult:
        """Run the LLM on the given messages."""

    @abstractmethod
    def get_context_size(self) -> int:
        """Run the LLM on the given prompts."""

    @abstractmethod
    def tokenizer_encode(self, text: str) -> List[int]:
        """Run the LLM on the given prompts."""

    @abstractmethod
    def tokenizer_decode(self, tokens: List[int]) -> str:
        """Run the LLM on the given prompts."""

    def get_num_tokens(self, text: str) -> int:
        """Get the number of tokens present in the text."""
        return len(self.tokenizer_encode(text))

    def get_num_tokens_from_messages(self, messages: List[BaseMessage]) -> int:
        """Get the number of tokens in the message."""
        return sum([self.get_num_tokens(get_buffer_string([m])) for m in messages])

    def _combine_llm_outputs(self, llm_outputs: List[Optional[dict]]) -> dict:
        return {}

    def _isChatCompletion(self, prompt: Union[List[BaseMessage], str]) -> bool:
        if isinstance(prompt, str):
            return False
        elif isListBaseMessage(prompt):
            return True
        else:
            raise ValueError(
                "Argument 'prompt' is expected to be of type List[BaseMessage] or str, received"
                f" argument of type {type(prompt)}."
            )

    def generate_prompt(
        self,
        prompts: List[str],
        stop: Optional[List[str]] = None,
        callbacks: Callbacks = None,
        *,
        tags: Optional[List[str]] = None,
        **kwargs: Any,
    ) -> LLMResult:
        """Run the LLM on the given prompt and input."""
        # If string is passed in directly no errors will be raised but outputs will
        # not make sense.
        if not isinstance(prompts, list):
            raise ValueError(
                "Argument 'prompts' is expected to be of type List[str], received"
                f" argument of type {type(prompts)}."
            )
        params = self.dict()
        params["stop"] = stop
        options = {"stop": stop}
        (
            existing_prompts,
            llm_string,
            missing_prompt_idxs,
            missing_prompts,
        ) = get_prompts(params, prompts)
        disregard_cache = self.cache is not None and not self.cache
        callback_manager = CallbackManager.configure(
            callbacks, self.callbacks, self.verbose, tags, self.tags
        )
        new_arg_supported = inspect.signature(self._generate_prompt).parameters.get(
            "run_manager"
        )
        if llmadapter.llm_cache is None or disregard_cache:
            # This happens when llmadapter.cache is None, but self.cache is True
            if self.cache is not None and self.cache:
                raise ValueError(
                    "Asked to cache, but no cache found at `llmadapter.cache`."
                )
            run_manager = callback_manager.on_llm_start(
                dumpd(self), prompts, invocation_params=params, options=options
            )
            try:
                output = (
                    self._generate_prompt(
                        prompts, stop=stop, run_manager=run_manager, **kwargs
                    )
                    if new_arg_supported
                    else self._generate_prompt(prompts, stop=stop, **kwargs)
                )
            except (KeyboardInterrupt, Exception) as e:
                run_manager.on_llm_error(e)
                raise e
            run_manager.on_llm_end(output)
            if run_manager:
                output.run = RunInfo(run_id=run_manager.run_id)
            return output
        if len(missing_prompts) > 0:
            run_manager = callback_manager.on_llm_start(
                dumpd(self),
                missing_prompts,
                invocation_params=params,
                options=options,
            )
            try:
                new_results = (
                    self._generate_prompt(
                        missing_prompts, stop=stop, run_manager=run_manager, **kwargs
                    )
                    if new_arg_supported
                    else self._generate_prompt(missing_prompts, stop=stop, **kwargs)
                )
            except (KeyboardInterrupt, Exception) as e:
                run_manager.on_llm_error(e)
                raise e
            run_manager.on_llm_end(new_results)
            llm_output = update_cache(
                existing_prompts, llm_string, missing_prompt_idxs, new_results, prompts
            )
            run_info = None
            if run_manager:
                run_info = RunInfo(run_id=run_manager.run_id)
        else:
            llm_output = {}
            run_info = None
        generations = [existing_prompts[i] for i in range(len(prompts))]
        return LLMResult(generations=generations, llm_output=llm_output, run=run_info)

    async def agenerate_prompt(
        self,
        prompts: List[str],
        stop: Optional[List[str]] = None,
        callbacks: Callbacks = None,
        *,
        tags: Optional[List[str]] = None,
        **kwargs: Any,
    ) -> LLMResult:
        """Run the LLM on the given prompt and input."""
        params = self.dict()
        params["stop"] = stop
        options = {"stop": stop}
        (
            existing_prompts,
            llm_string,
            missing_prompt_idxs,
            missing_prompts,
        ) = get_prompts(params, prompts)
        disregard_cache = self.cache is not None and not self.cache
        callback_manager = AsyncCallbackManager.configure(
            callbacks, self.callbacks, self.verbose, tags, self.tags
        )
        new_arg_supported = inspect.signature(self._agenerate_prompt).parameters.get(
            "run_manager"
        )
        if llmadapter.llm_cache is None or disregard_cache:
            # This happens when llmadapter.cache is None, but self.cache is True
            if self.cache is not None and self.cache:
                raise ValueError(
                    "Asked to cache, but no cache found at `llmadapter.cache`."
                )
            run_manager = await callback_manager.on_llm_start(
                dumpd(self), prompts, invocation_params=params, options=options
            )
            try:
                output = (
                    await self._agenerate_prompt(
                        prompts, stop=stop, run_manager=run_manager, **kwargs
                    )
                    if new_arg_supported
                    else await self._agenerate_prompt(prompts, stop=stop, **kwargs)
                )
            except (KeyboardInterrupt, Exception) as e:
                await run_manager.on_llm_error(e, verbose=self.verbose)
                raise e
            await run_manager.on_llm_end(output, verbose=self.verbose)
            if run_manager:
                output.run = RunInfo(run_id=run_manager.run_id)
            return output
        if len(missing_prompts) > 0:
            run_manager = await callback_manager.on_llm_start(
                dumpd(self),
                missing_prompts,
                invocation_params=params,
                options=options,
            )
            try:
                new_results = (
                    await self._agenerate_prompt(
                        missing_prompts, stop=stop, run_manager=run_manager, **kwargs
                    )
                    if new_arg_supported
                    else await self._agenerate_prompt(missing_prompts, stop=stop, **kwargs)
                )
            except (KeyboardInterrupt, Exception) as e:
                await run_manager.on_llm_error(e)
                raise e
            await run_manager.on_llm_end(new_results)
            llm_output = update_cache(
                existing_prompts, llm_string, missing_prompt_idxs, new_results, prompts
            )
            run_info = None
            if run_manager:
                run_info = RunInfo(run_id=run_manager.run_id)
        else:
            llm_output = {}
            run_info = None
        generations = [existing_prompts[i] for i in range(len(prompts))]
        return LLMResult(generations=generations, llm_output=llm_output, run=run_info)

    def generate_messages(
        self,
        messages: List[List[BaseMessage]],
        stop: Optional[List[str]] = None,
        callbacks: Callbacks = None,
        *,
        tags: Optional[List[str]] = None,
        **kwargs: Any,
    ) -> LLMResult:
        """Top Level call"""

        params = self.dict()
        params["stop"] = stop
        options = {"stop": stop}

        (
            existing_prompts,
            llm_string,
            missing_prompt_idxs,
            missing_prompts,
        ) = get_chat_prompts(params, messages)
        disregard_cache = self.cache is not None and not self.cache

        callback_manager = CallbackManager.configure(
            callbacks,
            self.callbacks,
            self.verbose,
            tags,
            self.tags,
        )
        run_manager = callback_manager.on_chat_model_start(
            dumpd(self), messages, invocation_params=params, options=options
        )

        new_arg_supported = inspect.signature(self._generate_messages).parameters.get(
            "run_manager"
        )
        if llmadapter.llm_cache is None or disregard_cache:
            # This happens when langchain.cache is None, but self.cache is True
            if self.cache is not None and self.cache:
                raise ValueError(
                    "Asked to cache, but no cache found at `langchain.cache`."
                )
            try:
                results: List[ChatResult] = [
                    self._generate_messages(m, stop=stop, run_manager=run_manager, **kwargs)
                    if new_arg_supported
                    else self._generate_messages(m, stop=stop)
                    for m in messages
                ]
                llm_outputs = [res.llm_output for res in results]
            except (KeyboardInterrupt, Exception) as e:
                run_manager.on_llm_error(e)
                raise e
        else:
            # use cache
            if len(missing_prompts) > 0:
                try:
                    new_results = [
                        self._generate_messages(m, stop=stop, run_manager=run_manager, **kwargs)
                        if new_arg_supported
                        else self._generate_messages(m, stop=stop)
                        for m in missing_prompts
                    ]
                except (KeyboardInterrupt, Exception) as e:
                    run_manager.on_llm_error(e)
                    raise e

                llm_outputs = update_chat_cache(
                    existing_prompts,
                    llm_string,
                    missing_prompt_idxs,
                    new_results,
                    messages,
                )
                # Combine cached results and new results
                results_dict = {
                    **existing_prompts,
                    **dict(zip(missing_prompt_idxs, new_results)),
                }
                results = [result for _, result in sorted(results_dict.items())]
            else:
                llm_outputs = []
                # All prompts were caches, so we construct results solely from cache
                results = [r for _, r in existing_prompts.items()]
        llm_output = self._combine_llm_outputs(llm_outputs)
        generations = [res.generations for res in results]
        output = LLMResult(generations=generations, llm_output=llm_output)
        run_manager.on_llm_end(output)
        if run_manager:
            output.run = RunInfo(run_id=run_manager.run_id)
        return output

    async def agenerate_messages(
        self,
        messages: List[List[BaseMessage]],
        stop: Optional[List[str]] = None,
        callbacks: Callbacks = None,
        *,
        tags: Optional[List[str]] = None,
        **kwargs: Any,
    ) -> LLMResult:
        """Top Level call"""
        params = self.dict()
        params["stop"] = stop
        options = {"stop": stop}

        (
            existing_prompts,
            llm_string,
            missing_prompt_idxs,
            missing_prompts,
        ) = get_chat_prompts(params, messages)
        disregard_cache = self.cache is not None and not self.cache
        callback_manager = AsyncCallbackManager.configure(
            callbacks,
            self.callbacks,
            self.verbose,
            tags,
            self.tags,
        )
        run_manager = await callback_manager.on_chat_model_start(
            dumpd(self), messages, invocation_params=params, options=options
        )

        new_arg_supported = inspect.signature(self._agenerate_messages).parameters.get(
            "run_manager"
        )
        if llmadapter.llm_cache is None or disregard_cache:
            # This happens when llmadapter.cache is None, but self.cache is True
            if self.cache is not None and self.cache:
                raise ValueError(
                    "Asked to cache, but no cache found at `llmadapter.cache`."
                )
            try:
                results = await asyncio.gather(
                    *[
                        self._agenerate_messages(m, stop=stop, run_manager=run_manager, **kwargs)
                        if new_arg_supported
                        else self._agenerate_messages(m, stop=stop)
                        for m in messages
                    ]
                )
                llm_outputs = [res.llm_output for res in results]
            except (KeyboardInterrupt, Exception) as e:
                await run_manager.on_llm_error(e)
                raise e
        else:
            # use cache
            if len(missing_prompts) > 0:
                try:
                    new_results = await asyncio.gather(
                        *[
                            self._agenerate_messages(m, stop=stop, run_manager=run_manager, **kwargs)
                            if new_arg_supported
                            else self._agenerate_messages(m, stop=stop)
                            for m in missing_prompts
                        ]
                    )
                except (KeyboardInterrupt, Exception) as e:
                    run_manager.on_llm_error(e)
                    raise e
                llm_outputs = update_chat_cache(
                    existing_prompts,
                    llm_string,
                    missing_prompt_idxs,
                    new_results,
                    messages,
                )
                # Combine cached results and new results
                results_dict = {
                    **existing_prompts,
                    **dict(zip(missing_prompt_idxs, new_results)),
                }
                results = [result for _, result in sorted(results_dict.items())]
            else:
                llm_outputs = []
                # All prompts were caches, so we construct results solely from cache
                results = [r for _, r in existing_prompts.items()]
        llm_output = self._combine_llm_outputs(llm_outputs)
        generations = [res.generations for res in results]
        output = LLMResult(generations=generations, llm_output=llm_output)
        await run_manager.on_llm_end(output)
        if run_manager:
            output.run = RunInfo(run_id=run_manager.run_id)
        return output

    def generate(
        self,
        prompts: Union[List[List[BaseMessage]], List[str]],
        stop: Optional[List[str]] = None,
        callbacks: Callbacks = None,
        *,
        tags: Optional[List[str]] = None,
        **kwargs: Any,
    ) -> LLMResult:
        if all(isinstance(prompt, str) for prompt in prompts):
            return self.generate_prompt(prompts, stop=stop, callbacks=callbacks, tags=tags, **kwargs)
        elif all(isListBaseMessage(prompt) for prompt in prompts):
            return self.generate_messages(prompts, stop=stop, callbacks=callbacks, tags=tags, **kwargs)
        else:
            raise ValueError(
                "Argument 'prompts' is expected to be of type List[List[BaseMessage]] or List[str], received"
                f" argument of type {type(prompts)}."
            )

    async def agenerate(
        self,
        prompts: Union[List[List[BaseMessage]], List[str]],
        stop: Optional[List[str]] = None,
        callbacks: Callbacks = None,
        *,
        tags: Optional[List[str]] = None,
        **kwargs: Any,
    ) -> LLMResult:
        if all(isinstance(prompt, str) for prompt in prompts):
            return await self.agenerate_prompt(prompts, stop=stop, callbacks=callbacks, tags=tags, **kwargs)
        elif all(isListBaseMessage(prompt) for prompt in prompts):
            return await self.agenerate_messages(prompts, stop=stop, callbacks=callbacks, tags=tags, **kwargs)
        else:
            raise ValueError(
                "Argument 'prompts' is expected to be of type List[List[BaseMessage]] or List[str], received"
                f" argument of type {type(prompts)}."
            )

    def predict_prompt(
        self,
        prompt: str,
        stop: Optional[List[str]] = None,
        callbacks: Callbacks = None,
        **kwargs: Any,
    ) -> str:
        """Check Cache and run the LLM on the given prompt and input."""
        if not isinstance(prompt, str):
            raise ValueError(
                "Argument `prompt` is expected to be a string. Instead found "
                f"{type(prompt)}."
            )
        return (
            self.generate([prompt], stop=stop, callbacks=callbacks, **kwargs)
            .generations[0][0]
            .text
        )

    def predict_messages(
        self,
        messages: List[BaseMessage],
        stop: Optional[List[str]] = None,
        callbacks: Callbacks = None,
        **kwargs: Any,
    ) -> str:
        """Check Cache and run the LLM on the given prompt and input."""
        if not isListBaseMessage(messages):
            raise ValueError(
                "Argument `messages` is expected to be a List[BaseMessage]. Instead found "
                f"{type(messages)}."
            )
        generation = self.generate([messages], stop=stop, callbacks=callbacks, **kwargs ).generations[0][0]
        if isinstance(generation, ChatGeneration):
            return generation.message.content
        else:
            raise ValueError("Unexpected generation type")

    def predict(
        self,
        prompt: Union[List[BaseMessage], str],
        stop: Optional[List[str]] = None,
        callbacks: Callbacks = None,
        **kwargs: Any,
    ) -> str:
        """Check Cache and run the LLM on the given prompt and input."""
        if self._isChatCompletion(prompt):
            return self.predict_messages(prompt, stop, callbacks, **kwargs)
        else:
            return self.predict_prompt(prompt, stop, callbacks, **kwargs)

    async def apredict_prompt(
        self,
        prompt: str,
        stop: Optional[List[str]] = None,
        callbacks: Callbacks = None,
        **kwargs: Any,
    ) -> str:
        """Check Cache and run the LLM on the given prompt and input."""
        if not isinstance(prompt, str):
            raise ValueError(
                "Argument `prompt` is expected to be a string. Instead found "
                f"{type(prompt)}."
            )
        result = await self.agenerate([prompt], stop=stop, callbacks=callbacks, **kwargs)
        return result.generations[0][0].text

    async def apredict_messages(
        self,
        messages: List[BaseMessage],
        stop: Optional[List[str]] = None,
        callbacks: Callbacks = None,
        **kwargs: Any,
    ) -> str:
        """Check Cache and run the LLM on the given prompt and input."""
        if not isListBaseMessage(messages):
            raise ValueError(
                "Argument `messages` is expected to be a List[BaseMessage]. Instead found "
                f"{type(messages)}."
            )
        generation = (await self.agenerate([messages], stop=stop, callbacks=callbacks, **kwargs)).generations[0][0]
        if isinstance(generation, ChatGeneration):
            return generation.message.content
        else:
            raise ValueError("Unexpected generation type")

    async def apredict(
        self,
        prompt: Union[List[BaseMessage], str],
        stop: Optional[List[str]] = None,
        callbacks: Callbacks = None,
        **kwargs: Any,
    ) -> str:
        """Check Cache and run the LLM on the given prompt and input."""
        if self._isChatCompletion(prompt):
            return await self.apredict_messages(prompt, stop, callbacks, **kwargs)
        else:
            return await self.apredict_prompt(prompt, stop, callbacks, **kwargs)

    def update_custom_cache(
        self,
        prompt: Union[List[BaseMessage], str],
        content: str,
        stop: Optional[List[str]] = None,
    ) -> None:
        params = self.dict()
        params["stop"] = stop
        llm_string = str(sorted([(k, v) for k, v in params.items()]))
        if self._isChatCompletion(prompt):
            chat_generation = ChatGeneration(message=AIMessage(content=content))
            if llmadapter.llm_cache is not None:
                llmadapter.llm_cache.update(
                    chat_history_as_string(prompt), llm_string, [chat_generation]
                )
            else:
                raise ValueError("llm cache is none")
        else:
            generation = Generation(text=content)
            if llmadapter.llm_cache is not None:
                llmadapter.llm_cache.update(
                    prompt, llm_string, [generation]
                )
            else:
                raise ValueError("llm cache is none")

    @property
    def _identifying_params(self) -> Mapping[str, Any]:
        """Get the identifying parameters."""
        return {}

    def __str__(self) -> str:
        """Get a string representation of the object for printing."""
        cls_name = f"\033[1m{self.__class__.__name__}\033[0m"
        return f"{cls_name}\nParams: {self._identifying_params}"

    @property
    @abstractmethod
    def _llm_type(self) -> str:
        """Return type of llm."""

    def dict(self, **kwargs: Any) -> Dict:
        """Return a dictionary of the LLM."""
        starter_dict = dict(self._identifying_params)
        starter_dict["_type"] = self._llm_type
        return starter_dict

    def save(self, file_path: Union[Path, str]) -> None:
        """Save the LLM.

        Args:
            file_path: Path to file to save the LLM to.

        Example:
        .. code-block:: python

            llm.save(file_path="path/llm.yaml")
        """
        # Convert file to Path object.
        if isinstance(file_path, str):
            save_path = Path(file_path)
        else:
            save_path = file_path

        directory_path = save_path.parent
        directory_path.mkdir(parents=True, exist_ok=True)

        # Fetch dictionary to save
        prompt_dict = self.dict()

        if save_path.suffix == ".json":
            with open(file_path, "w") as f:
                json.dump(prompt_dict, f, indent=4)
        elif save_path.suffix == ".yaml":
            with open(file_path, "w") as f:
                yaml.dump(prompt_dict, f, default_flow_style=False)
        else:
            raise ValueError(f"{save_path} must be json or yaml")