"""Client for interacting with LLMs."""

from typing import Any, Optional

import openai
from promptdown import StructuredPrompt

from fakedin.config import settings, validate_settings


class LLMClient:
    """Client for generating text via OpenAI API."""

    def __init__(self, model: Optional[str] = None):
        """Initialize the LLM client.

        Args:
            model: The model to use. Defaults to the one in settings.
        """
        validate_settings()
        self.client = openai.OpenAI(api_key=settings.openai_api_key)
        self.model = model or settings.openai_model

    def generate_from_promptdown(
        self, prompt_file: str, variables: dict[str, Any]
    ) -> str:
        """Generate text using a promptdown file.

        Args:
            prompt_file: Name of the promptdown file (without extension).
            variables: Variables to use in the prompt.

        Returns:
            Generated text.
        """
        try:
            prompt_path = settings.get_prompt_path(prompt_file)

            # Load the structured prompt from the file
            structured_prompt = StructuredPrompt.from_promptdown_file(str(prompt_path))

            # Apply template values to the prompt
            structured_prompt.apply_template_values(variables)

            # Convert to chat completion messages format
            messages = structured_prompt.to_chat_completion_messages()

            # Generate the response using the model
            return self.generate_with_messages(messages)
        except FileNotFoundError:
            raise FileNotFoundError(f"Prompt file not found: {prompt_file}.prompt.md")
        except Exception as e:
            raise RuntimeError(f"Error generating from promptdown: {str(e)}") from e

    def generate_with_messages(self, messages: list[dict[str, Any]]) -> str:
        """Generate text using the OpenAI API with formatted messages.

        Args:
            messages: The messages to send to the API in chat format.

        Returns:
            Generated text.
        """
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,  # type: ignore
                temperature=0.7,
            )

            # Extract the generated text from the response
            return response.choices[0].message.content or ""
        except Exception as e:
            raise RuntimeError(f"Error generating text: {str(e)}") from e

    def generate(self, prompt: str) -> str:
        """Generate text using the OpenAI API with a simple prompt.

        Args:
            prompt: The prompt to send to the API.

        Returns:
            Generated text.
        """
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": prompt},
                ],
                temperature=0.7,
            )

            # Extract the generated text from the response
            return response.choices[0].message.content or ""
        except Exception as e:
            raise RuntimeError(f"Error generating text: {str(e)}") from e
