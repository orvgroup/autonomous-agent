
"""OpenAI model integration for the ORVGROUP agent."""

import os

from openai import OpenAI

from agent.config import load_config


def generate_response(prompt: str) -> str:
    """Send a prompt to the configured AI model."""

    api_key = os.getenv("OPENAI_API_KEY")

    if not api_key:
        raise RuntimeError(
            "OPENAI_API_KEY environment variable is not configured."
        )

    if not prompt.strip():
        raise ValueError("Prompt cannot be empty.")

    config = load_config()
    client = OpenAI(api_key=api_key)

    response = client.responses.create(
        model=config.model,
        input=prompt,
    )

    return response.output_text
