import unittest
from pathlib import Path

from fakedin.cli import build_parser


class TestCliParser(unittest.TestCase):
    def setUp(self) -> None:
        self.parser = build_parser()

    def test_resume_defaults(self) -> None:
        args = self.parser.parse_args(["resume", "2"])

        self.assertEqual(args.command, "resume")
        self.assertEqual(args.count, 2)
        self.assertEqual(args.format, "markdown")
        self.assertEqual(args.output, Path("output"))

    def test_job_defaults(self) -> None:
        args = self.parser.parse_args(["job", "3"])

        self.assertEqual(args.command, "job")
        self.assertEqual(args.count, 3)
        self.assertEqual(args.output, Path("output"))

    def test_resumes_for_job_args(self) -> None:
        args = self.parser.parse_args(
            [
                "resumes-for-job",
                "jobs/sample_job.md",
                "4",
                "--format",
                "pdf",
                "--output",
                "./custom_output",
            ]
        )

        self.assertEqual(args.command, "resumes-for-job")
        self.assertEqual(args.job_description_file, Path("jobs/sample_job.md"))
        self.assertEqual(args.count, 4)
        self.assertEqual(args.format, "pdf")
        self.assertEqual(args.output, Path("custom_output"))


if __name__ == "__main__":
    unittest.main()
