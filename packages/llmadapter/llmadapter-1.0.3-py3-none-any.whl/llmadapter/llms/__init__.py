"""Wrappers on top of large language models APIs."""
from typing import Dict, Type

from llmadapter.llms.base import BaseLLM
from llmadapter.llms.openai import OpenAI

__all__ = [
    "OpenAI",
]

supported_type_list = [
    "openai",
]

type_to_cls_dict: Dict[str, Type[BaseLLM]] = {
    "openai": OpenAI,
}
