from __future__ import annotations

import requests

from shorts_pilot.generator.notify import alert
from shorts_pilot.generator.settings import Settings


def _settings(
    *,
    token: str = "123:ABC",
    chat_id: str = "-100123",
    prefix: str = "test",
) -> Settings:
    return Settings(
        api_key="sk-test",
        base_url="https://api.openai.com/v1",
        model="gpt-4o-mini",
        telegram_token=token,
        telegram_chat_id=chat_id,
        telegram_prefix=prefix,
        generate_count=21,
        refill_threshold=10,
        scan_dirs=[],
        langs={},
        jobs_dir=None,
        seen_dir=None,
    )


def test_sends_to_telegram_api(monkeypatch):
    calls = []

    def fake_post(url, **kw):
        calls.append({"url": url, "json": kw.get("json")})
        return type("R", (), {"ok": True})()

    monkeypatch.setattr("shorts_pilot.generator.notify.requests.post", fake_post)
    alert("hello", _settings())
    assert len(calls) == 1
    assert "api.telegram.org/bot123:ABC/sendMessage" in calls[0]["url"]
    assert "[test] hello" in calls[0]["json"]["text"]


def test_missing_token_skips(monkeypatch):
    calls = []

    def fake_post(url, **kw):
        calls.append(1)

    monkeypatch.setattr("shorts_pilot.generator.notify.requests.post", fake_post)
    alert("hi", _settings(token=""))
    assert calls == []


def test_missing_chat_id_skips(monkeypatch):
    calls = []

    def fake_post(url, **kw):
        calls.append(1)

    monkeypatch.setattr("shorts_pilot.generator.notify.requests.post", fake_post)
    alert("hi", _settings(chat_id=""))
    assert calls == []


def test_exception_is_swallowed(monkeypatch):
    def boom(*a, **kw):
        raise requests.ConnectionError("down")

    monkeypatch.setattr("shorts_pilot.generator.notify.requests.post", boom)
    alert("hi", _settings())  # Does not raise


# ponytail: reused Settings structure already has all required fields
