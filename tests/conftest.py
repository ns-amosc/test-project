# tests/conftest.py
"""
pytest configuration and shared fixtures
"""
import pytest
from form.fake_auth_app import FakeAuthApp


@pytest.fixture
def fake_auth_app():
    return FakeAuthApp()
