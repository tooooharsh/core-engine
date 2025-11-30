# Core Engine

A core engine implementation using langgraph and LangChain.

## Setup

1. Install uv if not already installed:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

2. Create a virtual environment and install dependencies:

```bash
uv venv
source .venv/bin/activate  # On Unix/macOS
uv pip install -e ".[dev]"
```

## Development

- Use `uv pip install <package>` to add new dependencies
- Run tests with `pytest`
- Format code with `black .`
- Sort imports with `isort .`
- Type check with `mypy .`

## Managing Dependencies

- To add a new dependency: `uv pip install <package>`
- To update dependencies: `uv pip sync`
- To compile requirements: `uv pip compile pyproject.toml`
