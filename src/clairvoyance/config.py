"""Configuration management for Clairvoyance."""

from __future__ import annotations

import os
from dataclasses import dataclass


@dataclass
class Config:
    """Application configuration loaded from environment variables."""

    discord_token: str

    @classmethod
    def from_env(cls) -> Config:
        """Load configuration from environment variables.

        Returns:
            Config instance with values from environment.

        Raises:
            ValueError: If required environment variables are missing.
        """
        discord_token = os.environ.get("DISCORD_BOT_TOKEN", "")

        if not discord_token or not discord_token.strip():
            msg = "DISCORD_BOT_TOKEN environment variable is required"
            raise ValueError(msg)

        return cls(discord_token=discord_token)
