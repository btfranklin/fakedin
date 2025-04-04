#!/usr/bin/env python3
"""
Generate fake job descriptions using FakedIn.

Usage:
    python generate_job.py <count> [--output OUTPUT_DIR]

Arguments:
    count               Number of job descriptions to generate
    --output, -o        Output directory (default: ./output)

Example:
    python generate_job.py 5
    python generate_job.py 3 --output ./job_listings
"""

import argparse
import os
import sys
from pathlib import Path

from fakedin.job_generator import JobOpeningGenerator


def main():
    """Generate fake job descriptions based on command line arguments."""
    parser = argparse.ArgumentParser(description="Generate fake job descriptions")

    parser.add_argument(
        "count", type=int, help="Number of job descriptions to generate"
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

    # Initialize generator and generate job descriptions
    try:
        generator = JobOpeningGenerator()
        generated_files = generator.generate_multiple(
            count=args.count, output_dir=args.output
        )

        # Print summary
        print(f"\nGenerated {len(generated_files)} job descriptions successfully.")
        print(f"Files saved to: {args.output}")

    except Exception as e:
        print(f"Error: {str(e)}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
