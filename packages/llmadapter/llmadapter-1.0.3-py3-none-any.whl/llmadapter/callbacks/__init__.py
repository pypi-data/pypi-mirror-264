"""Callback handlers that allow listening to events in llmadapter."""

from llmadapter.callbacks.aim_callback import AimCallbackHandler
from llmadapter.callbacks.argilla_callback import ArgillaCallbackHandler
from llmadapter.callbacks.arize_callback import ArizeCallbackHandler
from llmadapter.callbacks.clearml_callback import ClearMLCallbackHandler
from llmadapter.callbacks.comet_ml_callback import CometCallbackHandler
from llmadapter.callbacks.human import HumanApprovalCallbackHandler
from llmadapter.callbacks.manager import (
    get_openai_callback,
    tracing_enabled,
    wandb_tracing_enabled,
)
from llmadapter.callbacks.openai_info import OpenAICallbackHandler
from llmadapter.callbacks.stdout import StdOutCallbackHandler
from llmadapter.callbacks.streaming_aiter import AsyncIteratorCallbackHandler
from llmadapter.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from llmadapter.callbacks.streaming_stdout_final_only import (
    FinalStreamingStdOutCallbackHandler,
)

# now streamlit requires Python >=3.7, !=3.9.7 So, it is commented out here.
# from llmadapter.callbacks.streamlit import StreamlitCallbackHandler
from llmadapter.callbacks.wandb_callback import WandbCallbackHandler

__all__ = [
    "AimCallbackHandler",
    "ArgillaCallbackHandler",
    "ArizeCallbackHandler",
    "AsyncIteratorCallbackHandler",
    "ClearMLCallbackHandler",
    "CometCallbackHandler",
    "FinalStreamingStdOutCallbackHandler",
    "HumanApprovalCallbackHandler",
    "OpenAICallbackHandler",
    "StdOutCallbackHandler",
    "StreamingStdOutCallbackHandler",
    # now streamlit requires Python >=3.7, !=3.9.7 So, it is commented out here.
    # "StreamlitCallbackHandler",
    "WandbCallbackHandler",
    "get_openai_callback",
    "tracing_enabled",
    "wandb_tracing_enabled",
]
