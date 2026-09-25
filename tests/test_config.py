import pytest
from pydantic import ValidationError

from app.core.config import Settings


def test_local_env_allows_default_secret():
    assert Settings(ENV="local").SECRET_KEY == "change-me-in-env"


@pytest.mark.parametrize("env", ["staging", "production"])
def test_non_local_env_rejects_default_secret(env):
    with pytest.raises(ValidationError, match="SECRET_KEY"):
        Settings(ENV=env)


def test_non_local_env_rejects_short_secret():
    with pytest.raises(ValidationError, match="SECRET_KEY"):
        Settings(ENV="production", SECRET_KEY="too-short")


def test_non_local_env_accepts_strong_secret():
    assert Settings(ENV="production", SECRET_KEY="x" * 40).ENV == "production"
