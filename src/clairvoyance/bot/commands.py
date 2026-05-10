"""Discord bot command handlers."""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from discord import Message

if TYPE_CHECKING:
    from clairvoyance.bot.client import Bot

logger = logging.getLogger(__name__)

HELLO_RESPONSE = "Hello! I'm Clairvoyance, your D&D session witness. 🎲"


async def handle_hello(bot: Bot, message: Message) -> None:
    """Handle the !hello command.

    Responds with a greeting to confirm the bot is operational.

    Args:
        bot: The bot instance.
        message: The message that triggered the command.
    """
    if message.author.bot:
        return

    if message.content.strip().lower() == "!hello":
        logger.info("Hello command received from %s", message.author)
        await message.reply(HELLO_RESPONSE, mention_author=True)
