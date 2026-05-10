"""Tests for command registry."""

from __future__ import annotations

from clairvoyance.bot.commands import Command


class TestCommand:
    """Tests for Command enum."""

    def test_hello_command_name(self) -> None:
        """Test that HELLO command has correct name."""
        assert Command.HELLO.value == "!hello"

    def test_join_command_name(self) -> None:
        """Test that JOIN command has correct name."""
        assert Command.JOIN.value == "!join"

    def test_leave_command_name(self) -> None:
        """Test that LEAVE command has correct name."""
        assert Command.LEAVE.value == "!leave"

    def test_all_commands_defined(self) -> None:
        """Test that all expected commands are defined."""
        expected = {"!hello", "!join", "!leave"}
        actual = {cmd.value for cmd in Command}
        assert actual == expected

    def test_command_lookup_from_value(self) -> None:
        """Test that commands can be looked up by value."""
        assert Command.from_value("!hello") == Command.HELLO
        assert Command.from_value("!join") == Command.JOIN
        assert Command.from_value("!leave") == Command.LEAVE

    def test_command_lookup_returns_none_for_unknown(self) -> None:
        """Test that lookup returns None for unknown commands."""
        assert Command.from_value("!unknown") is None
        assert Command.from_value("hello") is None