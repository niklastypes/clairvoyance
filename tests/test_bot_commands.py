"""Tests for bot commands module."""

from __future__ import annotations

from unittest.mock import AsyncMock

import pytest

from clairvoyance.bot.client import Bot, create_bot
from clairvoyance.bot.commands import HELLO_RESPONSE, handle_hello
from tests.factories import BotConfigFactory


class MockAuthor:
    """Mock Discord message author."""

    def __init__(self, bot: bool = False, name: str = "TestUser", user_id: int = 12345) -> None:
        self.bot = bot
        self.name = name
        self.id = user_id


class MockMessage:
    """Mock Discord message for testing."""

    def __init__(
        self,
        content: str = "!hello",
        author_bot: bool = False,
        author_name: str = "TestUser",
        author_id: int = 12345,
    ) -> None:
        self.content = content
        self.author = MockAuthor(bot=author_bot, name=author_name, user_id=author_id)
        self.reply = AsyncMock()


@pytest.fixture
def bot() -> Bot:
    """Create a test bot instance."""
    config = BotConfigFactory.build()
    return create_bot(config)


@pytest.fixture
def mock_message() -> MockMessage:
    """Create a mock Discord message."""
    return MockMessage()


class TestHandleHello:
    """Tests for handle_hello command."""

    @pytest.mark.asyncio
    async def test_replies_with_hello_message(self, bot: Bot, mock_message: MockMessage) -> None:
        """Test that !hello command replies with greeting."""
        await handle_hello(bot, mock_message)

        mock_message.reply.assert_called_once_with(HELLO_RESPONSE, mention_author=True)

    @pytest.mark.asyncio
    async def test_ignores_bot_messages(self, bot: Bot, mock_message: MockMessage) -> None:
        """Test that bot ignores messages from other bots."""
        mock_message.author.bot = True

        await handle_hello(bot, mock_message)

        mock_message.reply.assert_not_called()

    @pytest.mark.asyncio
    async def test_ignores_non_hello_commands(self, bot: Bot, mock_message: MockMessage) -> None:
        """Test that non-!hello messages are ignored."""
        mock_message.content = "!other_command"

        await handle_hello(bot, mock_message)

        mock_message.reply.assert_not_called()

    @pytest.mark.asyncio
    async def test_handles_case_insensitive_hello(self, bot: Bot) -> None:
        """Test that !Hello and !HELLO are also handled."""
        message = MockMessage(content="!Hello")
        await handle_hello(bot, message)

        message.reply.assert_called_once()