from functools import lru_cache
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


BASE_DIR = Path(__file__).resolve().parents[2]


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=BASE_DIR / ".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    app_name: str = "BATMAN TECH Billing API"
    debug: bool = False
    secret_key: str = "change-me"
    access_token_expire_minutes: int = 60
    admin_username: str = "admin"
    admin_password: str = "change-me"

    database_url: str = "sqlite:///./batman_billing.db"

    mpesa_consumer_key: str = ""
    mpesa_consumer_secret: str = ""
    mpesa_shortcode: str = ""
    mpesa_passkey: str = ""
    mpesa_callback_url: str = "http://127.0.0.1:8000/payments/mpesa/callback"

    mikrotik_host: str = ""
    mikrotik_username: str = ""
    mikrotik_password: str = ""
    mikrotik_port: int = 8728

    radius_host: str = ""
    radius_secret: str = ""
    radius_auth_port: int = 1812
    radius_acct_port: int = 1813


@lru_cache
def get_settings() -> Settings:
    return Settings()
