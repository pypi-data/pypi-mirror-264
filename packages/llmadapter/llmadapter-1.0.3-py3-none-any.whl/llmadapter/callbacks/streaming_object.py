"""Callback handlers used in the app."""
from typing import Any

from llmadapter.callbacks.base import AsyncCallbackHandler
from llmadapter.schema import LLMResult

class AsyncObjectCallbackHandler(AsyncCallbackHandler):
    """Callback handler for streaming LLM responses."""

    def __init__(self, callObject):
        if not hasattr(callObject, 'step_process'):
            raise ValueError("Unexpected callobject: need function step_process")
        self.callObject = callObject

    async def on_llm_new_token(self, token: str, **kwargs: Any) -> None:
        await self.callObject.step_process(token=token, **kwargs)