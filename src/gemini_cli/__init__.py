from gemini_cli.cli import LLM_CLI

try:
    import google.generativeai
    from gemini_cli.gemini import (GeminiCLI, main)
except ModuleNotFoundError as e:
    pass
