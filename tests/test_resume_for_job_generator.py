from pathlib import Path

from fakedin.resume_for_job_generator import ResumeForJobGenerator


def test_generate_wraps_job_description_and_writes_file(
    tmp_path: Path,
) -> None:
    job_description_path = tmp_path / "job.md"
    job_description_path.write_text("Job details", encoding="utf-8")

    generator = ResumeForJobGenerator()

    generator.person_generator.generate_person = lambda: {
        "full_name": "Test Person",
        "age": 30,
        "email": "test@example.com",
        "phone_number": "555-555-5555",
        "location": "Testville, TS",
        "experience_years": 5,
        "experience_level": "Mid-Level",
    }

    captured = {}

    def _fake_generate(prompt_file: str, variables: dict) -> str:
        captured["prompt_file"] = prompt_file
        captured["variables"] = variables
        return "resume"

    generator.llm_client.generate_from_promptdown = _fake_generate

    output_path = generator.generate(
        job_description_path,
        output_format="markdown",
        output_dir=tmp_path,
    )

    assert captured["prompt_file"] == "resume_for_job"
    assert captured["variables"]["job_description"].startswith(
        "```markdown\nJob details\n```"
    )

    assert output_path.name == "test_person_for_job.md"
    assert output_path.exists()
    assert output_path.read_text(encoding="utf-8") == "resume"
