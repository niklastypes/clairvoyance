"""Discord bot client configuration and initialization."""

from __future__ import annotations

import logging

from discord import Activity, ActivityType, Client, Intents, Message
from pydantic import BaseModel, ConfigDict, Field, field_validator

logger = logging.getLogger(__name__)


class BotConfig(BaseModel):
    """Configuration for the Discord bot."""

    model_config = ConfigDict(frozen=True)

    token: str = Field(min_length=1)
    command_prefix: str = "!"
    activity: str = "D&D sessions"

    @field_validator("token")
    @classmethod
    def _validate_token(cls, v: str) -> str:
        """Ensure token is not empty or whitespace."""
        if not v or not v.strip():
            msg = "Token cannot be empty or whitespace"
            raise ValueError(msg)
        return v.strip()


class Bot(Client):
    """Discord bot client for Clairvoyance."""

    config: BotConfig

    def __init__(self, *, config: BotConfig) -> None:
        """Initialize the bot with configuration.

        Args:
            config: Bot configuration options.
        """
        self.config = config
        activity = Activity(
            type=ActivityType.watching,
            name=config.activity,
        )
        intents = _build_intents()
        super().__init__(
            intents=intents,
            activity=activity,
        )

    async def setup_hook(self) -> None:
        """Called when bot is ready to set up."""
        logger.info("Bot is setting up...")

    async def on_ready(self) -> None:
        """Called when bot successfully connects to Discord."""
        logger.info(f"Bot connected as {self.user} (ID: {self.user.id if self.user else 'unknown'})")

    async def on_message(self, message: Message) -> None:
        """Handle incoming messages.

        Args:
            message: The received message.
        """
        from clairvoyance.bot.commands import Command, handle_hello, handle_join, handle_leave

        command = Command.from_value(message.content)

        match command:
            case Command.HELLO:
                await handle_hello(self, message)
            case Command.JOIN:
                await handle_join(self, message)
            case Command.LEAVE:
                await handle_leave(self, message)
            case _:
                pass  # Unknown command, ignore


def _build_intents() -> Intents:
    """Build default intents with required permissions."""
    intents = Intents.default()
    intents.message_content = True
    intents.voice_states = True
    return intents


def create_bot(config: BotConfig) -> Bot:
    """Create and configure a bot instance.

    Args:
        config: Bot configuration options.

    Returns:
        Configured Bot instance ready to connect.
    """
    return Bot(config=config)
