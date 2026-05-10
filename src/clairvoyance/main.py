"""Main entry point for the Clairvoyance bot."""

from __future__ import annotations

import logging
import sys
from pathlib import Path

from dotenv import load_dotenv

from clairvoyance.bot.client import BotConfig, create_bot
from clairvoyance.config import Config

# Load .env file if present
load_dotenv(Path(__file__).parent.parent.parent / ".env")


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
        logging.error(f"Configuration error: {e}")
        sys.exit(1)

    bot_config = BotConfig(token=config.discord_token)
    bot = create_bot(bot_config)

    logging.info("Starting Clairvoyance bot...")
    bot.run(config.discord_token)


if __name__ == "__main__":
    main()
