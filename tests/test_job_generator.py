from pathlib import Path

from fakedin.job_generator import JobOpeningGenerator


def test_generate_writes_job_description(tmp_path: Path) -> None:
    generator = JobOpeningGenerator()

    generator.job_generator.generate_job = lambda: {
        "company_name": "Acme Co.",
        "career_field": "Software Engineer",
        "experience_level": "Mid-Level",
        "work_model": "Remote",
        "salary_range": "$80,000 - $100,000",
        "min_salary": 80000,
        "max_salary": 100000,
    }

    generator.llm_client.generate_from_promptdown = lambda *_args, **_kwargs: "job"

    output_path = generator.generate(output_dir=tmp_path)

    assert output_path.name == "acme_co_software_engineer_job.md"
    assert output_path.exists()
    assert output_path.read_text(encoding="utf-8") == "job"
