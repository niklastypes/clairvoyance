"""Tests for voice commands module."""

from __future__ import annotations

from unittest.mock import AsyncMock

import pytest

from clairvoyance.bot.commands import (
    JOIN_NO_VC_ERROR,
    LEAVE_NO_VC_ERROR,
    handle_join,
    handle_leave,
)
from tests.factories import BotConfigFactory


class MockVoiceChannel:
    """Mock Discord voice channel."""

    def __init__(self, id: int = 123, name: str = "Test VC") -> None:
        self.id = id
        self.name = name

    async def connect(self) -> None:
        """Mock connect method."""
        pass


class MockMember:
    """Mock Discord member."""

    def __init__(self, id: int = 456, name: str = "TestUser") -> None:
        self.id = id
        self.name = name
        self.bot = False
        self.voice: MockVoiceState | None = None


class MockTextMessage:
    """Mock Discord text message."""

    def __init__(
        self,
        content: str = "!join",
        author_bot: bool = False,
    ) -> None:
        self.content = content
        self.author = MockMember()
        self.author.bot = author_bot
        self.channel = MockTextChannel()
        self.reply = AsyncMock()

    async def reply(self, content: str, **kwargs: object) -> None:
        """Mock reply method."""
        self.reply(content)


class MockTextChannel:
    """Mock Discord text channel."""

    def __init__(self, id: int = 789, name: str = "general") -> None:
        self.id = id
        self.name = name


class MockVoiceState:
    """Mock Discord voice state."""

    def __init__(self, channel: MockVoiceChannel | None = None) -> None:
        self.channel = channel


class MockVoiceClient:
    """Mock Discord voice client."""

    def __init__(self, bot: MockBot | None = None) -> None:
        self._bot = bot

    async def disconnect(self) -> None:
        """Mock disconnect method."""
        if self._bot is not None:
            self._bot.voice_clients = []


class MockBot:
    """Mock bot for testing."""

    def __init__(self, config: object) -> None:
        self.config = config
        self.voice_clients: list[MockVoiceClient] = []

    @property
    def user(self) -> MockMember:
        return MockMember(id=999, name="ClairvoyanceBot")


@pytest.fixture
def bot() -> MockBot:
    """Create a test bot instance."""
    config = BotConfigFactory.build()
    return MockBot(config=config)


@pytest.fixture
def mock_message() -> MockTextMessage:
    """Create a mock text message."""
    return MockTextMessage()


class TestHandleJoin:
    """Tests for handle_join command."""

    @pytest.mark.asyncio
    async def test_join_joins_voice_channel_of_author(
        self, bot: MockBot, mock_message: MockTextMessage
    ) -> None:
        """Test that !join command causes bot to join author's voice channel."""
        # Arrange - member is in a voice channel
        mock_message.author.voice = MockVoiceState(channel=MockVoiceChannel())

        # Act
        result = await handle_join(bot, mock_message)

        # Assert - no error returned
        assert result is None

    @pytest.mark.asyncio
    async def test_join_ignores_bot_messages(
        self, bot: MockBot, mock_message: MockTextMessage
    ) -> None:
        """Test that bot ignores !join from other bots."""
        mock_message.author.bot = True

        result = await handle_join(bot, mock_message)

        assert result is None

    @pytest.mark.asyncio
    async def test_join_ignores_non_join_commands(
        self, bot: MockBot, mock_message: MockTextMessage
    ) -> None:
        """Test that non-!join messages are ignored."""
        mock_message.content = "!hello"

        result = await handle_join(bot, mock_message)

        assert result is None

    @pytest.mark.asyncio
    async def test_join_returns_error_when_user_not_in_vc(
        self, bot: MockBot, mock_message: MockTextMessage
    ) -> None:
        """Test that !join returns error when user is not in a voice channel."""
        # Arrange - member is NOT in a voice channel
        mock_message.author.voice = None

        # Act
        result = await handle_join(bot, mock_message)

        # Assert - error returned
        assert result == JOIN_NO_VC_ERROR
        mock_message.reply.assert_called()


class TestHandleLeave:
    """Tests for handle_leave command."""

    @pytest.mark.asyncio
    async def test_leave_leaves_voice_channel(
        self, bot: MockBot, mock_message: MockTextMessage
    ) -> None:
        """Test that !leave command causes bot to leave current voice channel."""
        # Arrange - bot is in a voice channel
        mock_vc = MockVoiceClient(bot=bot)
        bot.voice_clients = [mock_vc]
        mock_message.content = "!leave"

        # Act
        result = await handle_leave(bot, mock_message)

        # Assert - no error returned
        assert result is None
        assert len(bot.voice_clients) == 0

    @pytest.mark.asyncio
    async def test_leave_ignores_bot_messages(
        self, bot: MockBot, mock_message: MockTextMessage
    ) -> None:
        """Test that bot ignores !leave from other bots."""
        mock_message.author.bot = True
        mock_message.content = "!leave"

        result = await handle_leave(bot, mock_message)

        assert result is None

    @pytest.mark.asyncio
    async def test_leave_ignores_non_leave_commands(
        self, bot: MockBot, mock_message: MockTextMessage
    ) -> None:
        """Test that non-!leave messages are ignored."""
        mock_message.content = "!hello"

        result = await handle_leave(bot, mock_message)

        assert result is None

    @pytest.mark.asyncio
    async def test_leave_returns_error_when_not_in_vc(
        self, bot: MockBot, mock_message: MockTextMessage
    ) -> None:
        """Test that !leave returns error when bot is not in a voice channel."""
        mock_message.content = "!leave"

        result = await handle_leave(bot, mock_message)

        assert result == LEAVE_NO_VC_ERROR