import argparse
import google.generativeai as genai
import os 
import sys
import toml

def stream_generate_content(prompt, token):
    # 配置 token
    genai.configure(api_key=token)

    model = genai.GenerativeModel('gemini-pro')

    response = model.generate_content(
        prompt,
        stream = True,
    )
    for part in response:
        print(part.text, end='', flush=True)

def read_token_from_config():
    config_path = os.path.expanduser('~/.gemini.toml')
    try:
        config_data = toml.load(config_path)
        return config_data.get('token')
    except Exception as e:
        print(f"Error reading token from {config_path}: {e}")
        return None


def main():

    parser = argparse.ArgumentParser(description="Stream responses from Google Generative AI.")
    parser.add_argument('prompt', type=str, help="Prompt to send to the model", nargs='?', default=None)
    parser.add_argument('--token', type=str, help="API token for authentication", default=None)
    args = parser.parse_args()


    # 读取 prompt，支持从命令行参数或 stdin
    if args.prompt is not False:
        prompt = args.prompt if args.prompt is not True else sys.stdin.read().strip()
    else:
        parser.print_help()
        return

    # 读取 token，支持从命令行参数或配置文件
    token = args.token if args.token is not None else read_token_from_config()
    if token:
        stream_generate_content(prompt, token)
    else:
        print("Token not found. Please provide a token via --token argument or ensure your token is correctly set in ~/.gemini.toml.")

if __name__ == "__main__":
    main()
