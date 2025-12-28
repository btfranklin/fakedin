"""Module for generating realistic fake job openings."""

import os
from pathlib import Path

from fakedin.job_data_generator import JobGenerator
from fakedin.llm_client import LLMClient


class JobOpeningGenerator:
    """Generator for fake job openings."""

    def __init__(self):
        """Initialize the job opening generator."""
        self.job_generator = JobGenerator()
        self.llm_client = LLMClient()

    def generate(self, output_dir: Path | None = None) -> Path:
        """Generate a single job opening.

        Args:
            output_dir: Directory to save the job opening in. Defaults to the
                current directory.

        Returns:
            Path to the generated file.
        """
        # Generate random job details
        job = self.job_generator.generate_job()

        # Generate job opening content using LLM
        job_text = self.llm_client.generate_from_promptdown(
            "job_opening",
            job,
        )

        # Create output directory if it doesn't exist
        if output_dir is None:
            output_dir = Path.cwd()
        os.makedirs(output_dir, exist_ok=True)

        # Create sanitized filename
        sanitized_name = (
            job["company_name"].lower().replace(" ", "_").replace(".", "")
        )
        sanitized_field = (
            job["career_field"].lower().replace(" ", "_").replace(".", "")
        )

        output_path = output_dir / f"{sanitized_name}_{sanitized_field}_job.md"
        self._save_as_markdown(job_text, output_path)

        return output_path

    def generate_multiple(
        self, count: int, output_dir: Path | None = None
    ) -> list[Path]:
        """Generate multiple job openings.

        Args:
            count: Number of job openings to generate.
            output_dir: Directory to save the job openings in. Defaults to the
                current directory.

        Returns:
            List of paths to the generated files.
        """
        generated_files: list[Path] = []

        for i in range(count):
            file_path = self.generate(output_dir)
            generated_files.append(file_path)
            print(f"Generated job opening {i + 1}/{count}: {file_path}")

        return generated_files

    def _save_as_markdown(self, content: str, output_path: Path) -> None:
        """Save the job opening as a Markdown file."""
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(content)
