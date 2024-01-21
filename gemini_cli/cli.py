import argparse
import google.generativeai as genai
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

def stream_generate_content(prompt: str, token: str, config: Dict[str, Any]):
    # 配置 token
    genai.configure(api_key=token)

    model = genai.GenerativeModel('gemini-pro')

    response = model.generate_content(
        prompt,
        stream = True,
        safety_settings = safety_settings,
        generation_config = config,
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
    parser.add_argument('-f', '--config-file', type=str, help="Path to the config file", default='~/.gemini-cli.toml')
    args = parser.parse_args()



    # 读取 prompt，支持从命令行参数或 stdin
    if args.prompt is not False:
        prompt = args.prompt if args.prompt is not True else sys.stdin.read().strip()
    else:
        parser.print_help()
        return

    config = read_config(args.config_file)

    # 读取 token，支持从命令行参数或配置文件
    token = args.token if args.token is not None else config.get("token", None)
    if token:
        stream_generate_content(prompt, token, config.get("generation_config", None))
    else:
        print("Token not found. Please provide a token via --token argument or ensure your token is correctly set in ~/.gemini-cli.toml.")

if __name__ == "__main__":
    main()
