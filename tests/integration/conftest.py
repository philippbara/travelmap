import os
import pytest
from dotenv import load_dotenv


@pytest.fixture(scope="session", autouse=True)
def load_test_env():
    """
    Automatically load .env.test before any tests run.
    Must run before importing app.* modules.
    """
    env_path = os.path.join(os.path.dirname(__file__), "../..", ".env")
    load_dotenv(env_path)
