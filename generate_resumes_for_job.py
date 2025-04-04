#!/usr/bin/env python3
"""
Generate fake résumés tailored to a specific job description using FakedIn.

Usage:
    python generate_resumes_for_job.py <job_description_file> <count> [--format FORMAT] [--output OUTPUT_DIR]

Arguments:
    job_description_file  Path to the job description file (markdown format)
    count                 Number of résumés to generate
    --format, -f          Output format: 'pdf' or 'markdown' (default: markdown)
    --output, -o          Output directory (default: ./output)

Example:
    python generate_resumes_for_job.py output/acme_software_engineer_job.md 5
    python generate_resumes_for_job.py output/acme_software_engineer_job.md 3 --format pdf
    python generate_resumes_for_job.py output/acme_software_engineer_job.md 2 --output ./applicants --format pdf
"""

import argparse
import os
import sys
from pathlib import Path

from fakedin.resume_for_job_generator import ResumeForJobGenerator


def main():
    """Generate fake résumés tailored to a job description based on command line arguments."""
    parser = argparse.ArgumentParser(
        description="Generate fake résumés tailored to a job description"
    )

    parser.add_argument(
        "job_description_file",
        type=Path,
        help="Path to the job description file (markdown format)",
    )
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

    # Verify the job description file exists
    if not args.job_description_file.exists():
        print(
            f"Error: Job description file '{args.job_description_file}' not found.",
            file=sys.stderr,
        )
        sys.exit(1)

    # Create output directory if it doesn't exist
    try:
        os.makedirs(args.output, exist_ok=True)
        print(f"Output directory ready: {args.output}")
    except Exception as e:
        print(f"Error creating output directory: {str(e)}", file=sys.stderr)
        sys.exit(1)

    # Initialize generator and generate résumés tailored to the job
    try:
        generator = ResumeForJobGenerator()
        generated_files = generator.generate_multiple(
            job_description_path=args.job_description_file,
            count=args.count,
            output_format=args.format,
            output_dir=args.output,
        )

        # Print summary
        print(
            f"\nGenerated {len(generated_files)} résumés for job: {args.job_description_file.name}"
        )
        print(f"Files saved to: {args.output}")

    except Exception as e:
        print(f"Error: {str(e)}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
