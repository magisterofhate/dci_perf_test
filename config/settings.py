import os
from dataclasses import dataclass

from dotenv import load_dotenv


load_dotenv()


def _get_bool(name: str, default: bool = False) -> bool:
    value = os.getenv(name)
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "on"}


def _get_int(name: str, default: int) -> int:
    value = os.getenv(name)
    if value is None:
        return default
    return int(value)


@dataclass(frozen=True)
class ApiSettings:
    base_url: str
    login: str
    password: str
    verify_ssl: bool
    timeout: int


@dataclass(frozen=True)
class DBSettings:
    host: str
    port: int
    user: str
    password: str
    database: str


@dataclass(frozen=True)
class DebugSettings:
    response_log_enabled: bool
    db_logging_enabled: bool


@dataclass(frozen=True)
class Settings:
    api: ApiSettings
    db: DBSettings
    debug: DebugSettings

def _require(value: str, name: str) -> str:
    if not value:
        raise ValueError(f"Environment variable {name} is required")
    return value

def load_settings() -> Settings:
    return Settings(
        api=ApiSettings(
            base_url=_require(os.getenv("API_BASE_URL", ""), "API_BASE_URL"),
            login=_require(os.getenv("API_LOGIN", ""),"API_LOGIN"),
            password=_require(os.getenv("API_PASSWORD", ""), "API_PASSWORD"),
            verify_ssl=_get_bool("API_VERIFY_SSL", default=False),
            timeout=_get_int("API_TIMEOUT", default=60),
        ),
        db=DBSettings(
            host=os.getenv("DB_HOST", "172.31.36.82"),
            port=_get_int("DB_PORT", default=3306),
            user=os.getenv("DB_USER", "perf_user"),
            password=_require(os.getenv("DB_PASSWORD", ""), "DB_PASSWORD"),
            database=os.getenv("DB_NAME", "perf_tests"),
        ),
        debug=DebugSettings(
            response_log_enabled=_get_bool("DEBUG_RESPONSE_LOG", default=False),
            db_logging_enabled=_get_bool("ENABLE_DB_LOGGING", default=True),
        ),
    )