"""Tests for bot client module."""

from __future__ import annotations

import pytest

from clairvoyance.bot.client import BotConfig, Bot, create_bot
from tests.factories import BotConfigFactory


class TestBotConfig:
    """Tests for BotConfig Pydantic model."""

    def test_valid_config(self) -> None:
        """Test creating config with valid token."""
        config = BotConfig(token="valid_token_123")

        assert config.token == "valid_token_123"
        assert config.command_prefix == "!"
        assert config.activity == "D&D sessions"

    def test_custom_config(self) -> None:
        """Test creating config with custom values."""
        config = BotConfig(
            token="test_token",
            command_prefix="?",
            activity="recording",
        )

        assert config.token == "test_token"
        assert config.command_prefix == "?"
        assert config.activity == "recording"

    def test_empty_token_raises(self) -> None:
        """Test that empty token raises ValidationError."""
        with pytest.raises(ValueError):  # Pydantic raises ValueError for validation
            BotConfig(token="")

    def test_whitespace_token_raises(self) -> None:
        """Test that whitespace-only token raises ValidationError."""
        with pytest.raises(ValueError):
            BotConfig(token="   ")

    def test_factory_creates_valid_config(self) -> None:
        """Test that BotConfigFactory creates valid BotConfig instances."""
        config = BotConfigFactory.build()

        assert isinstance(config, BotConfig)
        assert config.token is not None
        assert config.command_prefix == "!"
        assert config.activity == "D&D sessions"

    def test_config_is_immutable(self) -> None:
        """Test that BotConfig instances are immutable after creation."""
        from pydantic import ValidationError

        config = BotConfigFactory.build()

        with pytest.raises(ValidationError):
            config.token = "new_token"

    def test_config_serialization(self) -> None:
        """Test that BotConfig can be serialized to dict."""
        config = BotConfigFactory.build()

        data = config.model_dump()
        assert data["token"] == config.token
        assert data["command_prefix"] == config.command_prefix
        assert data["activity"] == config.activity

    def test_config_from_dict(self) -> None:
        """Test that BotConfig can be created from a dictionary."""
        data = {
            "token": "dict_token_123",
            "command_prefix": "?",
            "activity": "custom",
        }
        config = BotConfig.model_validate(data)

        assert config.token == "dict_token_123"
        assert config.command_prefix == "?"
        assert config.activity == "custom"


class TestCreateBot:
    """Tests for create_bot factory function."""

    def test_creates_bot_with_correct_config(self) -> None:
        """Test that create_bot returns Bot with correct config."""
        config = BotConfigFactory.build()
        bot = create_bot(config)

        assert isinstance(bot, Bot)
        assert bot.config.token == config.token
        assert bot.activity is not None
        assert bot.activity.name == config.activity

    def test_creates_bot_with_custom_activity(self) -> None:
        """Test that create_bot respects custom activity."""
        config = BotConfig(token="test", activity="custom activity")
        bot = create_bot(config)

        assert bot.activity is not None
        assert bot.activity.name == "custom activity"

    def test_bot_has_message_content_intent(self) -> None:
        """Test that bot has message content intent enabled."""
        config = BotConfigFactory.build()
        bot = create_bot(config)

        assert bot.intents.message_content is True
