# Pydantic AI Streaming Example

This repository demonstrates how to implement streaming LLM responses with tool calls using Pydantic AI. It provides a practical example of building an extensible streaming solution that can be integrated into various backend/frontend workflows.

## Features

- Async streaming of LLM responses
- Tool call integration and handling
- Event type classification (display vs. debug)
- Structured message parsing
- Integration with Anthropic's Claude 3 Sonnet

## Prerequisites

- Python 3.12+
- An Anthropic API key

## Installation

1. Clone the repository and cd into pydantic-ai-streaming:
```bash
git clone https://github.com/bstuddard/python-examples.git
cd pydantic-ai-streaming
```

2. Create a virtual environment and activate it (venv, conda, etc)

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file in the root directory with your Anthropic API key:
```env
ANTHROPIC_API_KEY=your_api_key_here
```

## Project Structure
- src/
   - pydantic_stream_example.py # Main Pydantic AI streaming implementation
   - base_stream_example.py # Base API streaming example
   - schemas.py # Data models and schemas
- scripts/
   - base_model_test.ipynb # Base model testing notebook
   - pydantic_ai_base_test.ipynb # Pydantic AI testing notebook
- requirements.txt # Project dependencies

## Key Components

The project includes two main approaches to streaming:

1. **Base API Streaming** (`base_stream_example.py`)
   - Direct integration with Anthropic's API
   - Basic event handling and streaming

2. **Pydantic AI Streaming** (`pydantic_stream_example.py`)
   - Enhanced streaming with structured events
   - Tool call integration
   - Event type classification (display vs. debug)
   - Structured message parsing

## Dependencies

Key dependencies include:
- pydantic-ai[logfire]
- anthropic
- python-dotenv

See `requirements.txt` for a complete list of dependencies.

## Example Usage

The project includes Jupyter notebooks in the `scripts` directory that demonstrate both approaches:

- `base_model_test.ipynb`: Shows basic API streaming
- `pydantic_ai_base_test.ipynb`: Demonstrates Pydantic AI integration

## Environment Setup

Create a `.env` file in the root directory with:

```env
ANTHROPIC_API_KEY=your_api_key_here  # Required for Claude API access
```

## Additional Resources

- [Pydantic AI Documentation](https://ai.pydantic.dev/)
- [Anthropic API Documentation](https://docs.anthropic.com/)
- Blog post: [Streaming with Pydantic AI](https://datastud.dev/posts/pydantic-ai-streaming)

