"""Module for generating résumés tailored to job descriptions."""

import os
from pathlib import Path
from typing import Literal, Optional

from fakedin.resume_generator import ResumeGenerator
from fakedin.person_generator import PersonGenerator
from fakedin.llm_client import LLMClient


class ResumeForJobGenerator:
    """Generator for résumés tailored to job descriptions."""

    def __init__(self):
        """Initialize the resume for job generator."""
        self.person_generator = PersonGenerator()
        self.llm_client = LLMClient()
        self.resume_generator = ResumeGenerator()  # For saving functionality

    def generate(
        self,
        job_description_path: Path,
        output_format: Literal["pdf", "markdown"] = "markdown",
        output_dir: Optional[Path] = None,
    ) -> Path:
        """Generate a single résumé tailored to a job description.

        Args:
            job_description_path: Path to the job description file.
            output_format: Format to output the resume in ('pdf' or 'markdown').
            output_dir: Directory to save the resume in. Defaults to current directory.

        Returns:
            Path to the generated file.
        """
        # Read the job description
        with open(job_description_path, "r", encoding="utf-8") as f:
            job_description = f.read()

        # Generate random person details
        person = self.person_generator.generate_person()

        # Create parameters for the prompt
        params = {**person, "job_description": job_description}

        # Generate resume content using LLM
        resume_text = self.llm_client.generate_from_promptdown("resume_for_job", params)

        # Create output directory if it doesn't exist
        if output_dir is None:
            output_dir = Path.cwd()

        # Ensure the output directory exists
        os.makedirs(output_dir, exist_ok=True)

        # Create sanitized filename
        job_description_filename = job_description_path.stem
        sanitized_name = person["full_name"].lower().replace(" ", "_")

        # Save the resume in the requested format
        if output_format == "pdf":
            output_path = (
                output_dir / f"{sanitized_name}_for_{job_description_filename}.pdf"
            )
            try:
                self.resume_generator.save_as_pdf(resume_text, output_path, person)
            except Exception as e:
                print(f"Error creating PDF: {str(e)}")
                # Fallback to markdown
                markdown_path = (
                    output_dir / f"{sanitized_name}_for_{job_description_filename}.md"
                )
                self.resume_generator.save_as_markdown(resume_text, markdown_path)
                print(f"Saved as markdown file instead: {markdown_path}")
                output_path = markdown_path
        else:  # markdown
            output_path = (
                output_dir / f"{sanitized_name}_for_{job_description_filename}.md"
            )
            self.resume_generator.save_as_markdown(resume_text, output_path)

        return output_path

    def generate_multiple(
        self,
        job_description_path: Path,
        count: int,
        output_format: Literal["pdf", "markdown"] = "markdown",
        output_dir: Optional[Path] = None,
    ) -> list[Path]:
        """Generate multiple résumés tailored to a job description.

        Args:
            job_description_path: Path to the job description file.
            count: Number of résumés to generate.
            output_format: Format to output the resumes in ('pdf' or 'markdown').
            output_dir: Directory to save the resumes in. Defaults to current directory.

        Returns:
            List of paths to the generated files.
        """
        generated_files: list[Path] = []

        for i in range(count):
            try:
                file_path = self.generate(
                    job_description_path, output_format, output_dir
                )
                generated_files.append(file_path)
                print(f"Generated résumé {i+1}/{count} for job: {file_path}")
            except Exception as e:
                print(f"Error generating résumé {i+1} for job: {str(e)}")

        return generated_files
