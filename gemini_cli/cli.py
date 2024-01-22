import argparse
import google.generativeai as genai
import logging
import os 
import sys
import toml
import json
from typing import (Dict,Any)
from google.generativeai.types.generation_types import (GenerateContentResponse)

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

_logger = logging.getLogger("gemini-cli")

def stream_generate_chat(prompt: str, token: str, generation_config: Dict[str, Any], config, context):
    if not config:
        config = {}

    # 配置 token
    genai.configure(api_key=token)
    model = genai.GenerativeModel('gemini-pro')

    if not context:
        context = "You are a helpful assistant.";

    content = "Context: {context}\nUser: {prompt}\nBot: ".format(context = context, prompt = prompt)

    _logger.info("final prompt \n```\n" + content + "\n```")

    response = model.generate_content (
            content,
            stream = True,
            safety_settings = safety_settings,
            generation_config = generation_config
            )

    for part in response:
        print(part.text, end='', flush = True)

def stream_generate_content(prompt: str, token: str, generation_config: Dict[str, Any], config):
    if not config:
        config = {}

    # 配置 token
    genai.configure(api_key=token)

    model = genai.GenerativeModel('gemini-pro')

    response = model.generate_content(
            prompt,
            stream = True,
            safety_settings = safety_settings,
            generation_config = generation_config,
            )

    for part in response:
        print(part.text, end='', flush = True)

def read_config(custom_path):
    config_path = os.path.expanduser(custom_path)
    try:
        config_data = toml.load(config_path)
        return config_data;
    except Exception as e:
        print(f"Error reading token from {config_path}: {e}")
        return {}


def main():

    parser = argparse.ArgumentParser(description="Stream responses from Google Generative AI.")
    parser.add_argument('prompt', type=str, help="Prompt to send to the model", nargs='?', default=None)
    parser.add_argument('-t', '--token', type=str, help="API token for authentication", default=None)
    parser.add_argument('-s', '--context', type=str, help="context(context) prompt, optional", default=None)
    parser.add_argument('--system', dest='context', help='Alias for --context.')
    parser.add_argument('-f', '--config-file', type=str, help="Path to the config file", default='~/.config/gemini-cli.toml')
    parser.add_argument('-v', '--verbose', action='store_true',  help='Prompt string for the whale API')

    args = parser.parse_args()

    # 读取 prompt，支持从命令行参数或 stdin
    if args.verbose:
        logging.basicConfig(level=logging.INFO)
        _logger.setLevel(level=logging.INFO)
    if args.prompt is not False:
        prompt = args.prompt if args.prompt is not True else sys.stdin.read().strip()
        if not prompt:
            print("No prompt provided. Please provide a prompt to generate content.")
            parser.print_help()
            sys.exit(1)
    else:
        parser.print_help()
        return

    config = read_config(args.config_file)

    # 读取 token，支持从命令行参数或配置文件
    token = args.token if args.token is not None else config.get("token", None)
    context =  args.context if args.context is not None else config.get("context", None)
    if token:
        stream_generate_chat(prompt, token, config.get("generation_config", None), config=config, context = context)
    else:
        print("Token not found. Please provide a token via --token argument or ensure your token is correctly set in ~/.config/gemini-cli.toml.")

if __name__ == "__main__":
    main()
