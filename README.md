# Gemini CLI

[![PyPI](https://img.shields.io/pypi/v/gemini-cli)](https://pypi.org/project/gemini-cli)

Gemini is a Google Generative AI API for the terminal. It allows streaming responses from Google Generative AI models.

## Getting Started

### Installation

To install Gemini, run:

```bash
pip install gemini-cli
```

### Usage

To use Gemini, simply run the `gemini-cli` command followed by the prompt you want to send to the model. For example:

```bash
gemini-cli "Write a story about a robot who falls in love with a human."
```

This will send the prompt "Write a story about a robot who falls in love with a human." to the model, and the model's response will be printed to the terminal.

You can also provide a token for authentication using the `--token` flag. This is required if you want to use a model that is not available for public use. To get a token, [follow the instructions on the Google Generative AI website](https://generativelanguage.googleapis.com/start).

### Examples

Here are a few examples of how you can use Gemini:

* Write a story about a robot who falls in love with a human.
* Generate a poem about the beauty of nature.
* Translate a sentence from English to Spanish.
* Summarize a news article.
* Write a song about a lost love.

## Features

* **Stream responses:** Gemini streams responses from the model, so you can see the model's output as it is being generated.
* **Authentication:** Gemini supports authentication with a token, so you can use models that are not available for public use.
* **Command-line interface:** Gemini provides a simple command-line interface that is easy to use.

## Contributing

Gemini is open source and contributions are welcome. To contribute, please read the [contributing guidelines](CONTRIBUTING.md).

## License

Gemini is licensed under the MIT License.%
