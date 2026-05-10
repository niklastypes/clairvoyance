"""Discord bot command handlers."""

from __future__ import annotations

import logging
from enum import StrEnum
from typing import TYPE_CHECKING, Union

from discord import Message, VoiceChannel

if TYPE_CHECKING:
    from discord import Member

logger = logging.getLogger(__name__)


class Command(StrEnum):
    """Available bot commands."""

    HELLO = "!hello"
    JOIN = "!join"
    LEAVE = "!leave"

    @classmethod
    def from_value(cls, value: str) -> Union[Command, None]:
        """Look up a command by its string value.

        Args:
            value: The command string (e.g., "!hello")

        Returns:
            The Command enum member or None if not found.
        """
        normalized = value.strip().lower()
        for cmd in cls:
            if cmd.value == normalized:
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
        logger.info(f"Hello command received from {message.author}")
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
        logger.info(f"Join command from {author} failed: not in VC")
        await message.reply(JOIN_NO_VC_ERROR, mention_author=True)
        return JOIN_NO_VC_ERROR

    channel: VoiceChannel = author.voice.channel
    logger.info(f"Join command from {author}, connecting to {channel.name}")
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

    if bot.voice is None:
        logger.info(f"Leave command from {author} failed: not in VC")
        await message.reply(LEAVE_NO_VC_ERROR, mention_author=True)
        return LEAVE_NO_VC_ERROR

    logger.info(f"Leave command from {author}, disconnecting")
    await bot.voice.disconnect()
    bot.voice = None
    await message.reply(LEAVE_RESPONSE, mention_author=True)

    return None