"""Tests for configuration module."""

from __future__ import annotations

import os
from unittest.mock import patch

import pytest

from clairvoyance.config import Config


class TestConfig:
    """Tests for Config dataclass."""

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
