"""Configuration settings for FakedIn."""

import os
from pathlib import Path

import dotenv
from pydantic import BaseModel, Field

# Load environment variables from .env file
dotenv.load_dotenv()


class Settings(BaseModel):
    """Settings for the FakedIn application."""

    # OpenAI API configuration
    openai_api_key: str = Field(
        default_factory=lambda: os.getenv("OPENAI_API_KEY", "")
    )
    openai_model: str = Field(
        default_factory=lambda: os.getenv("OPENAI_MODEL", "gpt-5.2")
    )

    # Paths
    base_dir: Path = Field(default_factory=lambda: Path(__file__).parent)
    prompts_dir: Path = Field(
        default_factory=lambda: Path(__file__).parent / "prompts"
    )
    templates_dir: Path = Field(
        default_factory=lambda: Path(__file__).parent / "templates"
    )
    data_dir: Path = Field(
        default_factory=lambda: Path(__file__).parent / "data"
    )

    # Generation settings
    default_output_dir: Path = Field(
        default_factory=lambda: Path.cwd() / "output"
    )

    def get_prompt_path(self, prompt_name: str) -> Path:
        """Get the path to a prompt file."""
        return self.prompts_dir / f"{prompt_name}.prompt.md"


# Create a global settings instance
settings = Settings()


def validate_settings() -> None:
    """Validate that all required settings are configured."""
    if not settings.openai_api_key:
        message = (
            "OpenAI API key is not set. Please set the OPENAI_API_KEY "
            "environment variable or create a .env file with "
            "OPENAI_API_KEY=your_key"
        )
        raise ValueError(message)
