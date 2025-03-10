"""Module for generating realistic fake résumés."""

import os
from pathlib import Path
from typing import Any, Literal, Optional

from fpdf import FPDF  # Package name is fpdf2, but module name is fpdf

from fakedin.data_generator import PersonGenerator
from fakedin.llm_client import LLMClient


class ResumeGenerator:
    """Generator for fake résumés."""

    def __init__(self):
        """Initialize the resume generator."""
        self.person_generator = PersonGenerator()
        self.llm_client = LLMClient()

    def generate(
        self,
        output_format: Literal["pdf", "markdown"] = "markdown",
        output_dir: Optional[Path] = None,
    ) -> Path:
        """Generate a single résumé.

        Args:
            output_format: Format to output the resume in ('pdf' or 'markdown').
            output_dir: Directory to save the resume in. Defaults to current directory.

        Returns:
            Path to the generated file.
        """
        # Generate random person details
        person = self.person_generator.generate_person()

        # Generate resume content using LLM
        resume_text = self.llm_client.generate_from_promptdown("resume", person)

        # Create output directory if it doesn't exist
        if output_dir is None:
            output_dir = Path.cwd()
        os.makedirs(output_dir, exist_ok=True)

        # Create sanitized filename
        sanitized_name = person["full_name"].lower().replace(" ", "_")

        # Save the resume in the requested format
        if output_format == "pdf":
            output_path = output_dir / f"{sanitized_name}_resume.pdf"
            self._save_as_pdf(resume_text, output_path, person)
        else:  # markdown
            output_path = output_dir / f"{sanitized_name}_resume.md"
            self._save_as_markdown(resume_text, output_path)

        return output_path

    def generate_multiple(
        self,
        count: int,
        output_format: Literal["pdf", "markdown"] = "markdown",
        output_dir: Optional[Path] = None,
    ) -> list[Path]:
        """Generate multiple résumés.

        Args:
            count: Number of résumés to generate.
            output_format: Format to output the resumes in ('pdf' or 'markdown').
            output_dir: Directory to save the resumes in. Defaults to current directory.

        Returns:
            List of paths to the generated files.
        """
        generated_files = []

        for i in range(count):
            try:
                file_path = self.generate(output_format, output_dir)
                generated_files.append(file_path)
                print(f"Generated résumé {i+1}/{count}: {file_path}")
            except Exception as e:
                print(f"Error generating résumé {i+1}: {str(e)}")

        return generated_files

    def _save_as_markdown(self, content: str, output_path: Path) -> None:
        """Save the resume as a Markdown file."""
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(content)

    def _save_as_pdf(
        self, content: str, output_path: Path, person: dict[str, Any]
    ) -> None:
        """Save the resume as a PDF file."""
        pdf = FPDF()
        pdf.add_page()

        # Add title
        pdf.set_font("Arial", "B", 16)
        pdf.cell(0, 10, f"Resume: {person['full_name']}", 0, 1, "C")
        pdf.ln(10)

        # Add content
        pdf.set_font("Arial", "", 12)

        # Split content into paragraphs
        paragraphs = content.split("\n\n")

        for paragraph in paragraphs:
            # Handle markdown headers
            if paragraph.startswith("# "):
                pdf.set_font("Arial", "B", 14)
                pdf.multi_cell(0, 10, paragraph[2:])
                pdf.set_font("Arial", "", 12)
            elif paragraph.startswith("## "):
                pdf.set_font("Arial", "B", 12)
                pdf.multi_cell(0, 10, paragraph[3:])
                pdf.set_font("Arial", "", 12)
            elif paragraph.startswith("### "):
                pdf.set_font("Arial", "BI", 12)
                pdf.multi_cell(0, 10, paragraph[4:])
                pdf.set_font("Arial", "", 12)
            # Handle markdown lists
            elif paragraph.startswith("- "):
                lines = paragraph.split("\n")
                for line in lines:
                    pdf.multi_cell(0, 10, line)
            else:
                pdf.multi_cell(0, 10, paragraph)

            pdf.ln(5)

        # Save the PDF
        pdf.output(str(output_path))
