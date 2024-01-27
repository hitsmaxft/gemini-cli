import argparse
import google.generativeai as genai
import logging
import os 
import sys
import toml
import json
from typing import (Dict,Any)
from abc import ABC, abstractmethod
from google.generativeai.types.generation_types import (GenerateContentResponse)
from rich.console import Console
from rich.markdown import Markdown
from rich.live import Live
import logging


class LLM_CLI(ABC):

    def __init__(self, config_file: str, description: str="Stream responses from LLM."):
        self.config_file = config_file
        self.description = description
        self.console = Console()


    def read_config(self, custom_path):
        config_path = os.path.expanduser(custom_path)
        self.logger.info(f"config path is {config_path}");
        try:
            config_data = toml.load(config_path)
            return config_data;
        except Exception as e:
            print(f"Error reading token from {config_path}: {e}")
            return {}

    def printResponse(self, response, text_getter):
        config = self.config

        console = self.console

        if not config.get("markdown", False):
            self.logger.info("output in markdown format")
            if config.get("stream", False):
                for part in response:
                    print(text_getter(part), end="", flush=True)
            else:
                full_text = ""
                for part in response:
                    full_text += text_getter(part)
                print(full_text, end="", flush=True)
        else:
            if config.get("stream", False):
                with Live("", refresh_per_second=4) as live:
                    full_text = ""
                    for part in response:
                        full_text += text_getter(part)
                        live.update(Markdown(full_text))
                    live.update(Markdown(full_text))
            else:
                full_text = ""
                for part in response:
                    full_text += text_getter(part)
                console.print(Markdown(full_text))

    def argsParser(self):
        parser = argparse.ArgumentParser(description=self.description)
        parser.add_argument('prompt', type=str, help="Prompt to send to the model", nargs='?', default=None)
        parser.add_argument('-t', '--token', type=str, help="API token for authentication", default=None)
        parser.add_argument('-c', '--context', type=str, help="context(context) prompt, optional", default=None)
        parser.add_argument('-s', '--system', dest='context', help='Alias for --context.')
        parser.add_argument('-f', '--config-file', type=str, help=f"Path to the config file, use {self.config_file} by default.", default=self.config_file)
        parser.add_argument('-v', '--verbose', action='store_true',  help='Prompt string for the whale API')
        parser.add_argument('--stream', action='store_true',  help='stream output')
        parser.add_argument('--markdown', action='store_true', help='output markdown format', default=False)
        parser.add_argument('-n', '--limit',  type=int,  help='limit prompt length')
        self.configExtraParams(parser)
        return parser

    def configExtraParams(self, parser):
        pass

    @abstractmethod
    def stream_generate_content(self, prompt, token, generation_config, render_markdown):
        pass

    @abstractmethod
    def stream_generate_chat(self, prompt: str, token: str, generation_config: Dict[str, Any], config, context):
        pass

    def run(self):
        logger = self.logger
        parser = self.argsParser()

        args = parser.parse_args()

        # 读取 prompt，支持从命令行参数或 stdin
        if args.verbose:
            logging.basicConfig(level=logging.INFO)
            self.logger.setLevel(level=logging.INFO)
        if args.prompt is not False:
            prompt = args.prompt if args.prompt is not True else sys.stdin.read().strip()
            if not prompt:
                print("No prompt provided. Please provide a prompt to generate content.")
                parser.print_help()
                sys.exit(1)
        else:
            parser.print_help()
            return

        config = self.read_config(args.config_file)


        # 读取 token，支持从命令行参数或配置文件
        token = args.token if args.token is not None else config.get("token", None)
        context =  args.context if args.context is not None else config.get("context", None)

        if args.stream:
            config["stream"] = True

        if args.markdown:
            config["markdown"] = True

        logger.info(f"config is {json.dumps(config)}")


        self.config = config

        if token:
            self.stream_generate_chat(prompt, token, config.get("generation_config", None), config=config, context = context)
        else:
            print(f"Token not found. Please provide a token via --token argument or ensure your token is correctly set in {self.config_file}.")
            sys.exit(-1)