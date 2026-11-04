import pytest

from subs import create_app


def test_production_starts_without_redis(app_config: dict[str, object], monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr("subs.load_dotenv", lambda: None)
    monkeypatch.delenv("RATELIMIT_STORAGE_URI", raising=False)

    app = create_app(app_config | {"APP_ENV": "production"})

    assert app.test_client().get("/login").status_code == 200


def test_production_enables_secure_cookie(app_config: dict[str, object]) -> None:
    app = create_app(app_config | {"APP_ENV": "production"})

    assert app.config["SESSION_COOKIE_SECURE"] is True
