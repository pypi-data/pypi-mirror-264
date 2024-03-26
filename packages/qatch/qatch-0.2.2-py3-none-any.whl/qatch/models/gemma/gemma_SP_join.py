from __future__ import annotations

from typing import Any

import pandas as pd

from .abstract_gemma import AbstractGemma


class GemmaSP(AbstractGemma):
    @property
    def prompt(self):
        return [
            {"role": "user", "content":
                """I want you to act as a text to SQL model for tabular data.
                   I will pass you the schema of the table and one question.
                   I want you to parse the question into the SQL command.
                   The SQL command must be executable with the schema of the table.
                   Do not write explanations. Do not type commands. 
                   REPLY ONLY WITH THE SQL COMMAND.
                   This is an Example:
                   Table name: "body-builder", 
                    Schema: [Name, Surname], 
                    Questions: "Show all information about each body builder"
                    I want you to output:
                    "SELECT * FROM "body-builder""
                    """},
            {"role": "user", "content":
                'Table name: "student",'
                "Schema: [StudentID, Grade, PhoneNumbers]"
                'Question: "what are all the phone numbers?"'},
            {"role": "assistant",
             "content": 'SELECT "PhoneNumbers" FROM student'},
            {"role": "user", "content":
                'Table name: "student"'
                "Schema: [StudentID, Grade, PhoneNumbers]"
                'Question: "what is the average grade?"'},
            {"role": "assistant",
             "content": "SELECT AVG(Grade) FROM student"},
        ]

    @property
    def name(self):
        return 'Gemma_SP'

    def _normalize_output(self, text):
        return text

    def process_input(self, table: pd.DataFrame | None, db_table_schema: dict | None, query: str,
                      query_tbl_name: str | list[str]) -> Any | None:
        if not query_tbl_name:
            raise ValueError('For Semantic Parsing, it is need the table name '
                             'for the chatgpt input prompt')
        schema = table.columns.tolist()
        prompt = f'Table Name: "{query_tbl_name}",\nSchema: {schema},\nQuestion: "{query}"'
        prompt = [{"role": "user", "content": prompt}]
        messages = self.prompt + prompt
        model_input = self.pipeline.tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
        return model_input
