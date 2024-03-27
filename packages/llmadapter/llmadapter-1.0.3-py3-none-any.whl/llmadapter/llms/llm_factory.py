"""LLM Adapter."""
from pathlib import Path
from llmadapter.llms import supported_type_list, type_to_cls_dict
from typing import Any, List, Union
from llmadapter.llms.base import BaseLLM
from llmadapter.llms.loading import load_llm

class LLMFactory():
    @property
    def llm_type(self) -> List[str]:
        """Get the supported llm type."""
        return supported_type_list

    def create_llm(self, llm_type: str, **params: Any) -> BaseLLM:
        if llm_type not in type_to_cls_dict:
            raise ValueError(f"Loading {llm_type} LLM not supported")
        llm_cls = type_to_cls_dict[llm_type]
        return llm_cls(**params)

    def create_by_file(self, file: Union[str, Path]) -> BaseLLM:
        """yaml or json file path"""
        return load_llm(file)

# 创建单例对象
llm_factory = LLMFactory()
