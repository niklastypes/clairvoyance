"""Tests for configuration module."""

from __future__ import annotations

import os
from unittest.mock import patch

import pytest

from clairvoyance.config import Config
from tests.factories import ConfigFactory


class TestConfig:
    """Tests for Config Pydantic model."""

    def test_loads_from_environment(self) -> None:
        """Test loading config from environment variable."""
        with patch.dict(os.environ, {"DISCORD_BOT_TOKEN": "test_token_123"}):
            config = Config.from_env()

        assert config.discord_token == "test_token_123"

    def test_missing_token_raises(self) -> None:
        """Test that missing token raises ValueError."""
        with patch.dict(os.environ, {}, clear=True):
            with pytest.raises(
                ValueError, match="DISCORD_BOT_TOKEN environment variable is required"
            ):
                Config.from_env()

    def test_empty_token_raises(self) -> None:
        """Test that empty token raises ValueError."""
        with patch.dict(os.environ, {"DISCORD_BOT_TOKEN": ""}):
            with pytest.raises(
                ValueError, match="DISCORD_BOT_TOKEN environment variable is required"
            ):
                Config.from_env()

    def test_whitespace_token_raises(self) -> None:
        """Test that whitespace-only token raises ValueError."""
        with patch.dict(os.environ, {"DISCORD_BOT_TOKEN": "   "}):
            with pytest.raises(
                ValueError, match="DISCORD_BOT_TOKEN environment variable is required"
            ):
                Config.from_env()


class TestConfigModel:
    """Tests for Config model behavior."""

    def test_factory_creates_valid_config(self) -> None:
        """Test that ConfigFactory creates valid Config instances."""
        config = ConfigFactory.build()

        assert isinstance(config, Config)
        assert config.discord_token is not None
        assert len(config.discord_token) > 0

    def test_config_is_immutable(self) -> None:
        """Test that Config instances are immutable after creation."""
        from pydantic import ValidationError

        config = ConfigFactory.build()

        with pytest.raises(ValidationError):
            config.discord_token = "new_token"

    def test_config_serialization(self) -> None:
        """Test that Config can be serialized to dict."""
        config = ConfigFactory.build()

        data = config.model_dump()
        assert data["discord_token"] == config.discord_token