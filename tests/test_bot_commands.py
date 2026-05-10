"""Tests for bot commands module."""

from __future__ import annotations

from unittest.mock import AsyncMock, MagicMock

import pytest

from clairvoyance.bot.client import Bot, BotConfig, create_bot
from clairvoyance.bot.commands import HELLO_RESPONSE, handle_hello


@pytest.fixture
def bot() -> Bot:
    """Create a test bot instance."""
    config = BotConfig(token="test_token")
    return create_bot(config)


@pytest.fixture
def mock_message() -> MagicMock:
    """Create a mock message."""
    message = MagicMock()
    message.author.bot = False
    message.content = "!hello"
    message.reply = AsyncMock()
    return message


class TestHandleHello:
    """Tests for handle_hello command."""

    @pytest.mark.asyncio
    async def test_replies_with_hello_message(
        self, bot: Bot, mock_message: MagicMock
    ) -> None:
        """Test that !hello command replies with greeting."""
        await handle_hello(bot, mock_message)

        mock_message.reply.assert_called_once_with(HELLO_RESPONSE, mention_author=True)

    @pytest.mark.asyncio
    async def test_ignores_bot_messages(
        self, bot: Bot, mock_message: MagicMock
    ) -> None:
        """Test that bot ignores messages from other bots."""
        mock_message.author.bot = True

        await handle_hello(bot, mock_message)

        mock_message.reply.assert_not_called()

    @pytest.mark.asyncio
    async def test_ignores_non_hello_commands(
        self, bot: Bot, mock_message: MagicMock
    ) -> None:
        """Test that non-!hello messages are ignored."""
        mock_message.content = "!other_command"

        await handle_hello(bot, mock_message)

        mock_message.reply.assert_not_called()

    @pytest.mark.asyncio
    async def test_handles_case_insensitive_hello(
        self, bot: Bot, mock_message: MagicMock
    ) -> None:
        """Test that !Hello and !HELLO are also handled."""
        mock_message.content = "!Hello"

        await handle_hello(bot, mock_message)

        mock_message.reply.assert_called_once()
