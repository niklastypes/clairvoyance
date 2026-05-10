"""Tests for bot client module."""

from __future__ import annotations

import pytest

from clairvoyance.bot.client import BotConfig, Bot, create_bot


class TestBotConfig:
    """Tests for BotConfig dataclass."""

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
        """Test that empty token raises ValueError."""
        with pytest.raises(ValueError, match="Bot token is required"):
            BotConfig(token="")

    def test_whitespace_token_raises(self) -> None:
        """Test that whitespace-only token raises ValueError."""
        with pytest.raises(ValueError, match="Bot token is required"):
            BotConfig(token="   ")


class TestCreateBot:
    """Tests for create_bot factory function."""

    def test_creates_bot_with_correct_config(self) -> None:
        """Test that create_bot returns Bot with correct config."""
        config = BotConfig(token="test_token_123")
        bot = create_bot(config)

        assert isinstance(bot, Bot)
        assert bot.config.token == "test_token_123"
        assert bot.activity is not None
        assert bot.activity.name == "D&D sessions"

    def test_creates_bot_with_custom_activity(self) -> None:
        """Test that create_bot respects custom activity."""
        config = BotConfig(token="test", activity="custom activity")
        bot = create_bot(config)

        assert bot.activity is not None
        assert bot.activity.name == "custom activity"

    def test_bot_has_message_content_intent(self) -> None:
        """Test that bot has message content intent enabled."""
        config = BotConfig(token="test_token")
        bot = create_bot(config)

        assert bot.intents.message_content is True
