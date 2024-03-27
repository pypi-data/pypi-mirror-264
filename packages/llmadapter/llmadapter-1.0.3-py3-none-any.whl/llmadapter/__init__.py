"""Main entrypoint into package."""

from importlib import metadata
from typing import Optional
from llmadapter.cache import BaseCache
from llmadapter.llms import OpenAI

try:
    __version__ = metadata.version(__package__)
except metadata.PackageNotFoundError:
    # Case where package metadata is not available.
    __version__ = ""
del metadata  # optional, avoids polluting the results of dir(__package__)

verbose: bool = False
debug: bool = False
llm_cache: Optional[BaseCache] = None

__all__ = [
    "OpenAI",
]
