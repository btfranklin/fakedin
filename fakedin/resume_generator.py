"""Module for generating realistic fake résumés."""

import os
import re
from pathlib import Path
from typing import Any, Literal, Optional

from fpdf import FPDF  # type: ignore # Package name is fpdf2, but module name is fpdf

from fakedin.person_generator import PersonGenerator
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
            try:
                self.save_as_pdf(resume_text, output_path, person)
            except Exception as e:
                print(f"Error creating PDF: {str(e)}")
                # Fallback to markdown
                markdown_path = output_dir / f"{sanitized_name}_resume.md"
                self.save_as_markdown(resume_text, markdown_path)
                print(f"Saved as markdown file instead: {markdown_path}")
                raise
        else:  # markdown
            output_path = output_dir / f"{sanitized_name}_resume.md"
            self.save_as_markdown(resume_text, output_path)

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
        generated_files: list[Path] = []

        for i in range(count):
            try:
                file_path = self.generate(output_format, output_dir)
                generated_files.append(file_path)
                print(f"Generated résumé {i+1}/{count}: {file_path}")
            except Exception as e:
                print(f"Error generating résumé {i+1}: {str(e)}")

        return generated_files

    def save_as_markdown(self, content: str, output_path: Path) -> None:
        """Save the resume as a Markdown file."""
        # Ensure the parent directory exists
        os.makedirs(output_path.parent, exist_ok=True)

        with open(output_path, "w", encoding="utf-8") as f:
            f.write(content)

    def save_as_pdf(
        self, content: str, output_path: Path, person: dict[str, Any]
    ) -> None:
        """Save the resume as a PDF file with basic Markdown formatting support.

        Supported Markdown:
        - **bold** for bold text
        - _italic_ or *italic* for italic text
        - Headings (# H1, ## H2, ### H3)
        - List items (-, *)
        """
        # Ensure the parent directory exists
        os.makedirs(output_path.parent, exist_ok=True)

        # Create PDF
        pdf = FPDF()
        pdf.add_page()

        # Use Helvetica font which has good support for various characters
        pdf.set_font("Helvetica", size=12)

        # Preprocess the content to replace problematic Unicode characters
        content = self.sanitize_for_pdf(content)

        # Process the content by paragraphs for better formatting
        paragraphs = content.split("\n\n")

        for paragraph in paragraphs:
            # Handle headings with larger font size
            if paragraph.startswith("# "):
                pdf.set_font("Helvetica", style="B", size=18)
                pdf.multi_cell(0, 10, paragraph[2:])  # type: ignore
                pdf.set_font("Helvetica", size=12)
            elif paragraph.startswith("## "):
                pdf.set_font("Helvetica", style="B", size=14)
                pdf.multi_cell(0, 10, paragraph[3:])  # type: ignore
                pdf.set_font("Helvetica", size=12)
            elif paragraph.startswith("### "):
                pdf.set_font("Helvetica", style="B", size=12)
                pdf.multi_cell(0, 10, paragraph[4:])  # type: ignore
                pdf.set_font("Helvetica", size=12)
            # Handle lists
            elif paragraph.startswith("- ") or paragraph.startswith("* "):
                lines = paragraph.split("\n")
                for line in lines:
                    if line.startswith("- ") or line.startswith("* "):
                        # Use standard hyphen instead of bullet character
                        text = line[2:]
                        # Apply custom markdown parsing
                        text = self.parse_inline_formatting(text)
                        pdf.multi_cell(0, 10, f"- {text}")  # type: ignore
                    else:
                        text = self.parse_inline_formatting(line)
                        pdf.multi_cell(0, 10, text)  # type: ignore
            else:
                # Parse inline formatting for normal paragraphs
                text = self.parse_inline_formatting(paragraph)
                pdf.multi_cell(0, 10, text)  # type: ignore

            # Add some spacing between paragraphs
            pdf.ln(5)

        # Save the PDF
        pdf.output(str(output_path))

    def parse_inline_formatting(self, text: str) -> str:
        """Parse inline Markdown formatting and apply FPDF styling.

        This method handles:
        - **bold** or __bold__
        - *italic* or _italic_
        """
        # If text is None or empty, return empty string
        if not text:
            return ""

        # First, handle bold formatting
        # Find all occurrences of **text** or __text__
        bold_pattern = r"(\*\*|__)(.*?)\1"

        chunks = []
        last_end = 0

        for match in re.finditer(bold_pattern, text):
            # Add the text before the match
            chunks.append(text[last_end : match.start()])  # type: ignore

            # Add the bold text without the markers
            bold_text = match.group(2)
            chunks.append(bold_text)  # type: ignore

            last_end = match.end()

        # Add the remaining text
        chunks.append(text[last_end:])  # type: ignore

        # Join all parts
        result = "".join(chunks)  # type: ignore

        # Next, handle italic formatting
        # Find all occurrences of *text* or _text_
        italic_pattern = r"(\*|_)(.*?)\1"

        chunks = []
        last_end = 0

        for match in re.finditer(italic_pattern, result):
            # Add the text before the match
            chunks.append(result[last_end : match.start()])  # type: ignore

            # Add the italic text without the markers
            italic_text = match.group(2)
            chunks.append(italic_text)  # type: ignore

            last_end = match.end()

        # Add the remaining text
        chunks.append(result[last_end:])  # type: ignore

        # Join all parts
        result = "".join(chunks)  # type: ignore

        return result

    def sanitize_for_pdf(self, text: str) -> str:
        """Sanitize text for PDF output by replacing unsupported Unicode characters."""
        # Common problematic characters and their replacements
        replacements = {
            "\u2013": "-",  # en dash
            "\u2014": "--",  # em dash
            "\u2018": "'",  # left single quote
            "\u2019": "'",  # right single quote
            "\u201c": '"',  # left double quote
            "\u201d": '"',  # right double quote
            "\u2022": "-",  # bullet - replace with hyphen
            "\u2026": "...",  # ellipsis
            "\u00a0": " ",  # non-breaking space
            "\u2212": "-",  # minus sign
            "\u200b": "",  # zero width space
        }

        for char, replacement in replacements.items():
            text = text.replace(char, replacement)

        return text
