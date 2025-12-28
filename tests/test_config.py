import pytest

from fakedin import config


def test_get_prompt_path() -> None:
    path = config.settings.get_prompt_path("resume")
    assert path.name == "resume.prompt.md"


def test_validate_settings_raises_without_key(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(config.settings, "openai_api_key", "")
    with pytest.raises(ValueError):
        config.validate_settings()


def test_validate_settings_passes_with_key(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(config.settings, "openai_api_key", "test-key")
    config.validate_settings()
