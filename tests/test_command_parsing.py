"""Tests for command parsing with bot mentions."""

from __future__ import annotations

from clairvoyance.bot.commands import Command


class TestCommandWithMention:
    """Tests for command parsing when bot is mentioned."""

    def test_parse_command_with_bot_mention(self) -> None:
        """Test parsing command after bot mention."""
        message = "<@1503060612509335552> join"
        assert Command.from_value(message) == Command.JOIN

    def test_parse_command_with_bot_nickname_mention(self) -> None:
        """Test parsing command after bot nickname mention."""
        message = "<@!1503060612509335552> join"
        assert Command.from_value(message) == Command.JOIN

    def test_parse_command_without_mention(self) -> None:
        """Test parsing command without mention."""
        assert Command.from_value("join") == Command.JOIN
        assert Command.from_value("hello") == Command.HELLO
        assert Command.from_value("leave") == Command.LEAVE

    def test_parse_command_with_extra_text(self) -> None:
        """Test that commands with extra text after command are rejected."""
        # Extra text after command should not be accepted
        message = "<@1503060612509335552> join extra text"
        assert Command.from_value(message) is None

    def test_parse_unknown_command_with_mention(self) -> None:
        """Test that unknown commands return None."""
        message = "<@1503060612509335552> unknown"
        assert Command.from_value(message) is None

    def test_parse_hello_with_mention(self) -> None:
        """Test parsing hello command with mention."""
        message = "<@!1503060612509335552> hello"
        assert Command.from_value(message) == Command.HELLO

    def test_parse_leave_with_mention(self) -> None:
        """Test parsing leave command with mention."""
        message = "<@1503060612509335552> leave"
        assert Command.from_value(message) == Command.LEAVE
