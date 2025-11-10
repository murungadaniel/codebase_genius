# Codebase Documentation

## Overview
The `codebase_genius` repository hosts an AI-powered command-line interface (CLI) tool designed to assist developers in understanding, documenting, and improving their codebases. It leverages Large Language Models (LLMs) to analyze code, generate insights, identify potential improvements, and facilitate interaction with the codebase through natural language prompts.

## Repository Structure
The repository is structured as follows:

```
.
├── src/
│   └── codebase_genius/
│       ├── prompts/
│       │   ├── system_prompt.txt
│       │   └── user_prompt_template.txt
│       ├── __init__.py
│       ├── cli.py
│       ├── config.py
│       ├── core.py
│       └── utils.py
├── .gitignore
├── LICENSE
├── README.md
├── requirements.txt
└── setup.py
```

*   **`src/`**: Contains all the source code for the `codebase_genius` package.
*   **`src/codebase_genius/`**: The main Python package directory.
*   **`src/codebase_genius/prompts/`**: Stores text files defining the prompts used to interact with the LLMs.

## Key Files and Responsibilities

*   **`README.md`**: Provides a high-level overview of the project, setup instructions, and basic usage examples.
*   **`requirements.txt`**: Lists all Python dependencies required to run the project.
*   **`setup.py`**: Contains the necessary script for packaging and installing the `codebase_genius` project as a Python package.
*   **`src/codebase_genius/cli.py`**: Implements the command-line interface using a library like `click` or `argparse`, defining subcommands and their arguments. This is the entry point for users interacting with the tool.
*   **`src/codebase_genius/core.py`**: Houses the core logic of the application. This typically includes functions for interacting with LLM APIs, processing code input, and generating analysis or responses.
*   **`src/codebase_genius/utils.py`**: Contains utility functions that support the `core.py` and `cli.py` modules, such as file operations, string manipulation, or common helpers.
*   **`src/codebase_genius/config.py`**: Manages configuration settings for the application, such as API keys for LLMs, default model names, or other parameters. It likely loads these from environment variables.
*   **`src/codebase_genius/prompts/system_prompt.txt`**: Defines the initial, overarching instructions given to the LLM to set its role and context for the interaction.
*   **`src/codebase_genius/prompts/user_prompt_template.txt`**: Provides a template for constructing specific user queries that are sent to the LLM, often including placeholders for code snippets or specific questions.

## How to Run Locally

To run Codebase Genius locally, follow these steps:

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/murungadaniel/codebase_genius.git
    cd codebase_genius
    ```

2.  **Create and activate a virtual environment** (recommended):
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
    This will install all necessary Python packages.

4.  **Install the package in editable mode:**
    ```bash
    pip install -e .
    ```
    This allows you to run the `codebase_genius` command directly from your terminal.

5.  **Set up LLM API Key:**
    The tool likely requires an API key for a Large Language Model (e.g., OpenAI, Google Gemini, etc.). Refer to `src/codebase_genius/config.py` or the `README.md` for specific environment variable names or configuration methods. A common approach is:
    ```bash
    export OPENAI_API_KEY="your_api_key_here"
    # Or for other LLMs, e.g.,
    # export GOOGLE_API_KEY="your_api_key_here"
    ```
    *Note: The specific environment variable name depends on the LLM provider integrated and how it's configured in `config.py`.*

6.  **Run the CLI tool:**
    Once installed and configured, you can use the `codebase_genius` command. For example, to get help:
    ```bash
    codebase_genius --help
    ```
    Specific commands for analyzing code or generating documentation will be detailed in the `README.md` or via `codebase_genius <command> --help`.

## Possible Improvements

*   **Robust Configuration Management:** Enhance `config.py` to support multiple LLM providers easily and externalize sensitive credentials more securely (e.g., using a `.env` file or dedicated configuration manager).
*   **Comprehensive Testing:** Implement unit tests for `core.py`, `utils.py`, and `cli.py` to ensure reliability and prevent regressions. Integration tests for LLM interactions would also be valuable.
*   **Error Handling and User Feedback:** Improve error handling throughout the application, especially for API calls, and provide more informative and user-friendly messages for failures or unexpected behaviors.
*   **LLM Abstraction Layer:** Create a more explicit abstraction layer in `core.py` to make it easier to swap out or add new LLM providers (e.g., different models from OpenAI, Google, Anthropic, local models) without significant code changes.
*   **Caching Mechanism:** Implement caching for LLM responses or intermediate code analysis results to reduce API costs and improve performance for repeated queries on the same codebase.
*   **Codebase Traversal Strategy:** If not already robust, improve the code scanning and file selection logic to handle large repositories efficiently and respect `.gitignore` rules more strictly.
*   **Extensible Prompt Management:** Develop a more dynamic system for managing prompts, possibly allowing users to define or customize prompts via configuration files or command-line arguments.
*   **Interactive Mode:** Consider adding an interactive shell or session mode where users can have a multi-turn conversation with the AI about their codebase.
*   **Pre-commit Hooks and Linters:** Integrate tools like `black` for code formatting, `flake8` for linting, and `mypy` for static type checking to maintain code quality.