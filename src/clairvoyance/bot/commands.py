"""Discord bot command handlers."""

from __future__ import annotations

import logging
import re
from enum import StrEnum
from typing import TYPE_CHECKING, Union

from discord import Message, VoiceChannel

if TYPE_CHECKING:
    from discord import Member

logger = logging.getLogger(__name__)

# Pattern to match bot mentions: <@!123> or <@123> followed by optional whitespace
_MENTION_PATTERN = re.compile(r"^<@!?\d+>\s*")


class Command(StrEnum):
    """Available bot commands."""

    HELLO = "hello"  # Can be invoked as "!hello" or "hello"
    JOIN = "join"  # Can be invoked as "!join" or "join"
    LEAVE = "leave"  # Can be invoked as "!leave" or "leave"

    @classmethod
    def from_value(cls, value: str) -> Union[Command, None]:
        """Look up a command by its string value.

        Handles formats:
        - Bot mention format: "<@123> hello", "<@!123> join"
        - Direct commands: "hello", "join", "leave"

        Args:
            value: The message content (e.g., "hello" or "<@123> join")

        Returns:
            The Command enum member or None if not found.
        """
        normalized = value.strip().lower()
        # Strip bot mention prefix (e.g., "<@123456> ")
        normalized = _MENTION_PATTERN.sub("", normalized)
        # Now look for the command
        for cmd in cls:
            if normalized == cmd.value:
                return cmd
        return None


HELLO_RESPONSE = "Hello! I'm Clairvoyance, your D&D session witness. 🎲"
JOIN_RESPONSE = "Joining your voice channel! 🎙️"
JOIN_NO_VC_ERROR = "You're not in a voice channel. Join one first and try again."
LEAVE_RESPONSE = "Leaving the voice channel. 👋"
LEAVE_NO_VC_ERROR = "I'm not in a voice channel."


async def handle_hello(bot: object, message: Message) -> None:
    """Handle the !hello command.

    Responds with a greeting to confirm the bot is operational.

    Args:
        bot: The bot instance.
        message: The message that triggered the command.
    """
    if message.author.bot:
        return

    if Command.from_value(message.content) == Command.HELLO:
        logger.info("Hello command received from %s", message.author)
        await message.reply(HELLO_RESPONSE, mention_author=True)


async def handle_join(bot: object, message: Message) -> Union[str, None]:
    """Handle the !join command.

    Joins the voice channel of the user who sent the command.

    Args:
        bot: The bot instance.
        message: The message that triggered the command.

    Returns:
        Error message if user is not in a voice channel, None otherwise.
    """
    if message.author.bot:
        return None

    if Command.from_value(message.content) != Command.JOIN:
        return None

    author: Member = message.author

    if author.voice is None or author.voice.channel is None:
        logger.info("Join command from %s failed: not in VC", author)
        await message.reply(JOIN_NO_VC_ERROR, mention_author=True)
        return JOIN_NO_VC_ERROR

    channel: VoiceChannel = author.voice.channel
    logger.info("Join command from %s, connecting to %s", author, channel.name)
    await channel.connect()
    await message.reply(JOIN_RESPONSE, mention_author=True)

    return None


async def handle_leave(bot: object, message: Message) -> Union[str, None]:
    """Handle the !leave command.

    Disconnects from the current voice channel.

    Args:
        bot: The bot instance.
        message: The message that triggered the command.

    Returns:
        Error message if bot is not in a voice channel, None otherwise.
    """
    if message.author.bot:
        return None

    if Command.from_value(message.content) != Command.LEAVE:
        return None

    author = message.author

    voice_client = getattr(bot, "voice_clients", [])
    if not voice_client:
        logger.info("Leave command from %s failed: not in VC", author)
        await message.reply(LEAVE_NO_VC_ERROR, mention_author=True)
        return LEAVE_NO_VC_ERROR

    logger.info("Leave command from %s, disconnecting", author)
    await voice_client[0].disconnect()
    await message.reply(LEAVE_RESPONSE, mention_author=True)

    return None
