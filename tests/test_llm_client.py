from types import SimpleNamespace

import pytest

from fakedin import llm_client as llm_module
from fakedin.llm_client import LLMClient


class _DummyResponse:
    def __init__(self, content: str) -> None:
        self.choices = [SimpleNamespace(message=SimpleNamespace(content=content))]


class _DummyCompletions:
    def __init__(self, content: str) -> None:
        self._content = content
        self.calls = []

    def create(self, model: str, messages: list[dict[str, str]]):
        self.calls.append({"model": model, "messages": messages})
        return _DummyResponse(self._content)


class _DummyChat:
    def __init__(self, content: str) -> None:
        self.completions = _DummyCompletions(content)


class _DummyClient:
    def __init__(self, content: str) -> None:
        self.chat = _DummyChat(content)


def test_generate_with_messages_returns_content(monkeypatch: pytest.MonkeyPatch) -> None:
    dummy = _DummyClient("hello")
    monkeypatch.setattr(llm_module.openai, "OpenAI", lambda api_key: dummy)
    monkeypatch.setattr(llm_module.settings, "openai_api_key", "test-key")

    client = LLMClient(model="test-model")
    result = client.generate_with_messages([
        {"role": "user", "content": "hi"},
    ])

    assert result == "hello"
    assert dummy.chat.completions.calls


def test_generate_from_promptdown_missing_file(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(llm_module.openai, "OpenAI", lambda api_key: _DummyClient(""))
    monkeypatch.setattr(llm_module.settings, "openai_api_key", "test-key")

    client = LLMClient(model="test-model")

    with pytest.raises(FileNotFoundError):
        client.generate_from_promptdown("does_not_exist", {})
