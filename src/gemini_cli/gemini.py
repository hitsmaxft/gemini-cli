import argparse
import google.generativeai as genai
import logging
import os
import sys
import toml
import json
from typing import Dict, Any
from google.generativeai.types.generation_types import (GenerateContentResponse)
from google.ai.generativelanguage_v1beta.types.generative_service import Candidate
from rich.console import Console
from rich.markdown import Markdown
from rich.live import Live
from gemini_cli.cli import LLM_CLI

FinishReason = Candidate.FinishReason

DEFAULT_CONFIG_PATH: str = "~/.config/gemini-cli.toml"

safety_settings = [
    {
        "category": "HARM_CATEGORY_DANGEROUS",
        "threshold": "BLOCK_NONE",
    },
    {
        "category": "HARM_CATEGORY_HARASSMENT",
        "threshold": "BLOCK_NONE",
    },
    {
        "category": "HARM_CATEGORY_HATE_SPEECH",
        "threshold": "BLOCK_NONE",
    },
    {
        "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
        "threshold": "BLOCK_NONE",
    },
    {
        "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
        "threshold": "BLOCK_NONE",
    },
]

logger = logging.getLogger("gemini-cli")


class GeminiCLI(LLM_CLI):
    def __init__(self):
        super().__init__(
            "~/.config/gemini-cli.toml", "Stream responses from Google Generative AI."
        )
        self.logger = logger

    def stream_generate_chat(
        self,
        prompt: str,
        token: str,
        generation_config: Dict[str, Any],
        config,
        context,
    ):
        if not config:
            config = {}

        # 配置 token
        genai.configure(api_key=token)
        model = genai.GenerativeModel("gemini-pro")

        if not context:
            context = "You are a helpful assistant."

        content = "Context: {context}\nUser: {prompt}\nBot: ".format(
            context=context, prompt=prompt
        )

        self.logger.info("final prompt \n```\n" + content + "\n```")

        response = model.generate_content(
            content,
            stream=True,
            generation_config=generation_config,
        )

        def r_getter(r: GenerateContentResponse):
            if r._error:
                raise ValueError(r._error)
            elif r.candidates:
                c = r.candidates[0]
                if c.finish_reason != FinishReason.STOP:
                    text = FinishReason._value2member_map_.get(c.finish_reason).name
                    raise ValueError("stop by error, reason" + text)
                else:
                    return r.text
            else:
                raise ValueError("todo")

        self.printResponse(response,r_getter)

    def stream_generate_content(
        self, prompt: str, token: str, generation_config: Dict[str, Any], config
    ):
        if not config:
            config = {}

        # 配置 token
        genai.configure(api_key=token)

        model = genai.GenerativeModel("gemini-pro")

        response = model.generate_content(
            prompt,
            stream=True,
            safety_settings=safety_settings,
            generation_config=generation_config,
        )

        for part in response:
            print(part.text, end="", flush=True)

def main():
    GeminiCLI().run()