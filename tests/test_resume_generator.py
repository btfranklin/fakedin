from pathlib import Path

from fakedin.resume_generator import ResumeGenerator


def test_parse_inline_formatting_strips_markers() -> None:
    generator = ResumeGenerator()
    text = (
        "This is **bold** and _italic_ and *italic2* and __bold2__."
    )
    parsed = generator.parse_inline_formatting(text)

    assert "**" not in parsed
    assert "__" not in parsed
    assert "_" not in parsed
    assert "*" not in parsed
    assert parsed == "This is bold and italic and italic2 and bold2."


def test_sanitize_for_pdf_replaces_unicode() -> None:
    generator = ResumeGenerator()
    raw = (
        "Dash \u2013 dash \u2014 quote \u201cHi\u201d "
        "bullet \u2022 ellipsis \u2026"
    )
    sanitized = generator.sanitize_for_pdf(raw)

    assert "\u2013" not in sanitized
    assert "\u2014" not in sanitized
    assert "\u201c" not in sanitized
    assert "\u201d" not in sanitized
    assert "\u2022" not in sanitized
    assert "\u2026" not in sanitized
    assert "--" in sanitized
    assert "-" in sanitized
    assert "\"Hi\"" in sanitized
    assert "..." in sanitized


def test_save_as_markdown_writes_file(tmp_path: Path) -> None:
    generator = ResumeGenerator()
    output_path = tmp_path / "resume.md"
    generator.save_as_markdown("content", output_path)

    assert output_path.exists()
    assert output_path.read_text(encoding="utf-8") == "content"


def test_generate_pdf_falls_back_to_markdown(tmp_path: Path) -> None:
    generator = ResumeGenerator()

    generator.person_generator.generate_person = lambda: {
        "full_name": "Test Person",
        "age": 30,
        "email": "test@example.com",
        "phone_number": "555-555-5555",
        "city": "Testville",
        "state": "TS",
        "location": "Testville, TS",
        "career_field": "Software Engineer",
        "experience_years": 5,
        "experience_level": "Mid-Level",
    }

    def _fake_generate(*_args, **_kwargs) -> str:
        return "resume"

    generator.llm_client.generate_from_promptdown = _fake_generate

    def _raise_pdf(_content: str, _output_path: Path, _person: dict) -> None:
        raise RuntimeError("pdf failed")

    generator.save_as_pdf = _raise_pdf

    output_path = generator.generate(output_format="pdf", output_dir=tmp_path)

    assert output_path.suffix == ".md"
    assert output_path.exists()
    assert output_path.read_text(encoding="utf-8") == "resume"
