"""Main entry point for the Clairvoyance bot."""

from __future__ import annotations

import logging
import sys

from clairvoyance.bot.client import BotConfig, create_bot
from clairvoyance.config import Config


def main() -> None:
    """Run the Clairvoyance Discord bot."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        stream=sys.stdout,
    )

    try:
        config = Config.from_env()
    except ValueError as e:
        logging.error("Configuration error: %s", e)
        sys.exit(1)

    bot_config = BotConfig(token=config.discord_token)
    bot = create_bot(bot_config)

    logging.info("Starting Clairvoyance bot...")
    bot.run(config.discord_token)


if __name__ == "__main__":
    main()
