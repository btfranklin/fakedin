#!/usr/bin/env python3
"""
Generate fake résumés using FakedIn.

Usage:
    python generate_resume.py <count> [--format FORMAT] [--output OUTPUT_DIR]

Arguments:
    count               Number of résumés to generate
    --format, -f        Output format: 'pdf' or 'markdown' (default: markdown)
    --output, -o        Output directory (default: ./output)

Example:
    python generate_resume.py 5
    python generate_resume.py 3 --format pdf
    python generate_resume.py 2 --output ./my_resumes --format pdf
"""

import argparse
import os
import sys
from pathlib import Path

from fakedin.resume_generator import ResumeGenerator


def main():
    """Generate fake résumés based on command line arguments."""
    parser = argparse.ArgumentParser(description="Generate fake résumés")

    parser.add_argument("count", type=int, help="Number of résumés to generate")
    parser.add_argument(
        "--format",
        "-f",
        choices=["pdf", "markdown"],
        default="markdown",
        help="Output format: 'pdf' or 'markdown' (default: markdown)",
    )
    parser.add_argument(
        "--output",
        "-o",
        type=Path,
        default=Path("./output"),
        help="Output directory (default: ./output)",
    )

    args = parser.parse_args()

    # Create output directory if it doesn't exist
    try:
        os.makedirs(args.output, exist_ok=True)
        print(f"Output directory ready: {args.output}")
    except Exception as e:
        print(f"Error creating output directory: {str(e)}", file=sys.stderr)
        sys.exit(1)

    # Initialize generator and generate résumés
    try:
        generator = ResumeGenerator()
        generated_files = generator.generate_multiple(
            count=args.count, output_format=args.format, output_dir=args.output
        )

        # Print summary
        print(f"\nGenerated {len(generated_files)} résumés successfully.")
        print(f"Files saved to: {args.output}")

    except Exception as e:
        print(f"Error: {str(e)}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
