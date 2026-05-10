"""Discord bot client configuration and initialization."""

from __future__ import annotations

import logging
from dataclasses import dataclass

from discord import Activity, ActivityType, Client, Intents, Message

logger = logging.getLogger(__name__)


@dataclass
class BotConfig:
    """Configuration for the Discord bot."""

    token: str
    command_prefix: str = "!"
    activity: str = "D&D sessions"

    def _build_intents(self) -> Intents:
        """Build default intents with required permissions."""
        intents = Intents.default()
        intents.message_content = True
        return intents

    def __post_init__(self) -> None:
        """Validate configuration after initialization."""
        if not self.token or not self.token.strip():
            msg = "Bot token is required"
            raise ValueError(msg)


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
        super().__init__(
            intents=config._build_intents(),
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
        from clairvoyance.bot.commands import handle_hello

        await handle_hello(self, message)


def create_bot(config: BotConfig) -> Bot:
    """Create and configure a bot instance.

    Args:
        config: Bot configuration options.

    Returns:
        Configured Bot instance ready to connect.
    """
    return Bot(config=config)
