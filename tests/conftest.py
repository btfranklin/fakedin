import pytest

from fakedin import config


@pytest.fixture(autouse=True)
def _set_dummy_openai_key(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(config.settings, "openai_api_key", "test-key")
    yield
