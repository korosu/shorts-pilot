"""
notify.py — Telegram alerts for shorts-pilot.

Silently does nothing when TELEGRAM_TOKEN / TELEGRAM_CHAT_ID are not set in .env.
Never raises — a failed alert must not break the main run.
"""

from __future__ import annotations

import requests

from shorts_pilot.generator.settings import Settings


def alert(msg: str, settings: Settings) -> None:
    """Send a Telegram message if credentials are configured.

    Silently does nothing if credentials are missing — a missing/misconfigured
    notifier must never break a refill run.
    """
    if not settings.telegram_token or not settings.telegram_chat_id:
        return
    try:
        resp = requests.post(
            f"https://api.telegram.org/bot{settings.telegram_token}/sendMessage",
            json={"chat_id": settings.telegram_chat_id, "text": msg},
            timeout=10,
        )
        if not resp.ok:
            print(f"[shorts-pilot] Telegram returned {resp.status_code}: {resp.text[:200]}")
    except Exception as exc:
        print(f"[shorts-pilot] Telegram send failed: {exc}")
