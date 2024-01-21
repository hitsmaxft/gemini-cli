# Gemini CLI

[![PyPI](https://img.shields.io/pypi/v/gemini-cli)](https://pypi.org/project/gemini-cli)

Gemini is a Google Generative AI API for the terminal. It allows streaming responses from Google Generative AI models, designed to harness the capabilities of Google's Generative AI for creating rich, contextually relevant content. It's tailored for users seeking a straightforward, efficient means of leveraging AI for content generation, offering a seamless integration with Google's Generative AI API. With Gemini CLI, you can prompt the AI to craft stories, generate ideas, or even compose detailed texts, all from the comfort of your terminal.

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


    Prompt Input (param or stdin):
        Use Case: You're a writer looking for creative inspiration to start a new story. You can use the --prompt option to feed the AI a starting point, like --prompt "In a world where dragons are pets,", and let the AI generate an intriguing storyline continuation.

    API Token (--token):
        Use Case: As a developer working in different environments (development, staging, production), you might need to use different API tokens. The --token option allows you to specify the token directly in the command line for quick switches without changing the configuration file, like --token "your_api_token_here".

    Configuration File (-f/--config-file):
        Use Case: You're managing multiple projects with different configuration needs. The -f/--config-file option allows you to specify a custom path to a configuration file, enabling you to maintain separate configurations for each project. For instance, you can use --config-file "path/to/project_a_config.toml" for one project and switch to another with --config-file "path/to/project_b_config.toml".

    generation_config in TOML File:

        top_p, top_k, candidate_count, max_output_tokens, stop_sequences:
            Use Case: You're fine-tuning the AI's content generation for a chatbot application. You need the responses to be concise and contextually appropriate without veering off-topic. By adjusting top_p, top_k, candidate_count, max_output_tokens, and stop_sequences in the gemini.toml file, you can control the randomness, length, and termination of the AI-generated responses to fit the chatbot's conversational flow.


### Examples

Here are a few examples of how you can use Gemini:

* Write a story about a robot who falls in love with a human.
* Generate a poem about the beauty of nature.
* Translate a sentence from English to Spanish.
* Summarize a news article.
* Write a song about a lost love.

### How to Uage

## Features

* **Stream responses:** Gemini streams responses from the model, so you can see the model's output as it is being generated.
* **Authentication:** Gemini supports authentication with a token, so you can use models that are not available for public use.
* **Command-line interface:** Gemini provides a simple command-line interface that is easy to use.

## Contributing

Gemini is open source and contributions are welcome. To contribute, please read the [contributing guidelines](CONTRIBUTING.md).

## License

Gemini is licensed under the MIT License.%
