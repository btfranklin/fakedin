from fakedin.job_data_generator import JobGenerator


def test_generate_job_invariants() -> None:
    generator = JobGenerator()
    job = generator.generate_job()

    assert job["company_name"]
    assert job["career_field"]
    assert job["experience_level"] in generator.experience_levels
    assert job["work_model"] in generator.work_models

    assert job["min_salary"] <= job["max_salary"]
    expected_range = f"${job['min_salary']:,} - ${job['max_salary']:,}"
    assert job["salary_range"] == expected_range


def test_generate_company_name_non_empty() -> None:
    generator = JobGenerator()
    name = generator._generate_company_name()
    assert isinstance(name, str)
    assert name.strip()
