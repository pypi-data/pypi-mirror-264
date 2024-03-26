from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any

import pandas as pd
import torch
from huggingface_hub import login
from transformers import pipeline

from ..utils import check_prediction_list_dim


class AbstractGemma(ABC):
    def __init__(self, model_name="gg-hf/gemma-7b-it", hugging_face_token=None):
        login()
        self.pipeline = pipeline(
            "text-generation",
            model=model_name,
            model_kwargs={"torch_dtype": torch.bfloat16},
            device="cuda",
            # token=hugging_face_token
        )

    @property
    @abstractmethod
    def prompt(self):
        """Defines the prompt property in the child classes."""
        raise NotImplementedError

    @property
    @abstractmethod
    def name(self):
        """Defines the name property in the child classes."""
        raise NotImplementedError

    @abstractmethod
    def _normalize_output(self, text):
        """Provides the way to normalize output in the child classes."""
        raise NotImplementedError

    @abstractmethod
    def process_input(self,
                      table: pd.DataFrame | None,
                      db_table_schema: dict | None,
                      query: str,
                      query_tbl_name: str | list[str]) -> Any | None:
        """
        Defines the way to process input in the child classes.

        Args:
            table (pd.DataFrame, None): The input table data.
            db_table_schema (Dict, None, optional): The table schema. Defaults to None.
            query (str): The query to base the input processing on.
            query_tbl_name (str, List[str]): The query table name.

        Returns:
            Any: The processed data.
        """
        raise NotImplementedError

    def predict(self,
                table: pd.DataFrame | None,
                query: str,
                tbl_name: str | list[str],
                db_table_schema: dict | None = None) -> list[Any] | list[None]:
        """"""

        model_input = self.process_input(table, db_table_schema, query, tbl_name)
        if model_input is None:
            """Table is too large to be processed"""
            result = None
        else:
            result = self.pipeline(
                model_input,
                max_new_tokens=2048,
                add_special_tokens=True,
                do_sample=True,
                temperature=0.7,
                top_k=50,
                top_p=0.95
            )
            result = result[0]["generated_text"][len(model_input):]
            if 'SP' not in self.name:
                # only for QA models
                result = check_prediction_list_dim(result, check_llm=True)
        return result
