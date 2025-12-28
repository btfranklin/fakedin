"""Command-line interface for FakedIn."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from fakedin.job_generator import JobOpeningGenerator
from fakedin.resume_for_job_generator import ResumeForJobGenerator
from fakedin.resume_generator import ResumeGenerator


def build_parser() -> argparse.ArgumentParser:
    """Create the CLI argument parser."""
    parser = argparse.ArgumentParser(
        prog="fakedin",
        description="Generate fake resumes and job descriptions.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    resume_parser = subparsers.add_parser(
        "resume",
        help="Generate resumes.",
    )
    resume_parser.add_argument(
        "count",
        type=int,
        help="Number of resumes to generate",
    )
    resume_parser.add_argument(
        "--format",
        "-f",
        choices=["pdf", "markdown"],
        default="markdown",
        help="Output format: 'pdf' or 'markdown' (default: markdown)",
    )
    resume_parser.add_argument(
        "--output",
        "-o",
        type=Path,
        default=Path("./output"),
        help="Output directory (default: ./output)",
    )

    job_parser = subparsers.add_parser(
        "job",
        help="Generate job descriptions.",
    )
    job_parser.add_argument(
        "count",
        type=int,
        help="Number of job descriptions to generate",
    )
    job_parser.add_argument(
        "--output",
        "-o",
        type=Path,
        default=Path("./output"),
        help="Output directory (default: ./output)",
    )

    resumes_for_job_parser = subparsers.add_parser(
        "resumes-for-job",
        help="Generate resumes tailored to a job description.",
    )
    resumes_for_job_parser.add_argument(
        "job_description_file",
        type=Path,
        help="Path to the job description file (markdown format)",
    )
    resumes_for_job_parser.add_argument(
        "count",
        type=int,
        help="Number of resumes to generate",
    )
    resumes_for_job_parser.add_argument(
        "--format",
        "-f",
        choices=["pdf", "markdown"],
        default="markdown",
        help="Output format: 'pdf' or 'markdown' (default: markdown)",
    )
    resumes_for_job_parser.add_argument(
        "--output",
        "-o",
        type=Path,
        default=Path("./output"),
        help="Output directory (default: ./output)",
    )

    return parser


def _ensure_output_dir(output_dir: Path) -> None:
    try:
        output_dir.mkdir(parents=True, exist_ok=True)
        print(f"Output directory ready: {output_dir}")
    except Exception as exc:
        print(f"Error creating output directory: {exc}", file=sys.stderr)
        raise SystemExit(1)


def _ensure_job_description_file(path: Path) -> None:
    if not path.exists():
        print(
            f"Error: Job description file '{path}' not found.",
            file=sys.stderr,
        )
        raise SystemExit(1)


def _run_resume(count: int, output_format: str, output_dir: Path) -> None:
    _ensure_output_dir(output_dir)

    try:
        generator = ResumeGenerator()
        generated_files = generator.generate_multiple(
            count=count,
            output_format=output_format,
            output_dir=output_dir,
        )

        print(f"\nGenerated {len(generated_files)} resumes successfully.")
        print(f"Files saved to: {output_dir}")
    except Exception as exc:
        print(f"Error: {exc}", file=sys.stderr)
        raise SystemExit(1)


def _run_job(count: int, output_dir: Path) -> None:
    _ensure_output_dir(output_dir)

    try:
        generator = JobOpeningGenerator()
        generated_files = generator.generate_multiple(
            count=count,
            output_dir=output_dir,
        )

        print(
            f"\nGenerated {len(generated_files)} job descriptions "
            "successfully."
        )
        print(f"Files saved to: {output_dir}")
    except Exception as exc:
        print(f"Error: {exc}", file=sys.stderr)
        raise SystemExit(1)


def _run_resumes_for_job(
    job_description_file: Path,
    count: int,
    output_format: str,
    output_dir: Path,
) -> None:
    _ensure_job_description_file(job_description_file)
    _ensure_output_dir(output_dir)

    try:
        generator = ResumeForJobGenerator()
        generated_files = generator.generate_multiple(
            job_description_path=job_description_file,
            count=count,
            output_format=output_format,
            output_dir=output_dir,
        )

        print(
            f"\nGenerated {len(generated_files)} resumes for job: "
            f"{job_description_file.name}"
        )
        print(f"Files saved to: {output_dir}")
    except Exception as exc:
        print(f"Error: {exc}", file=sys.stderr)
        raise SystemExit(1)


def main(argv: list[str] | None = None) -> None:
    """Run the FakedIn CLI."""
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.command == "resume":
        _run_resume(args.count, args.format, args.output)
    elif args.command == "job":
        _run_job(args.count, args.output)
    elif args.command == "resumes-for-job":
        _run_resumes_for_job(
            args.job_description_file,
            args.count,
            args.format,
            args.output,
        )
    else:
        parser.print_help()
        raise SystemExit(1)


if __name__ == "__main__":
    main()
