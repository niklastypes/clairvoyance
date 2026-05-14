"""Configuration management for Clairvoyance."""

from __future__ import annotations

import os

from pydantic import BaseModel, ConfigDict, Field, field_validator


class Config(BaseModel):
    """Application configuration loaded from environment variables."""

    model_config = ConfigDict(frozen=True)

    discord_token: str = Field(min_length=1)

    @field_validator("discord_token")
    @classmethod
    def _validate_token(cls, v: str) -> str:
        """Ensure token is not empty or whitespace."""
        if not v or not v.strip():
            msg = "Token cannot be empty or whitespace"
            raise ValueError(msg)
        return v.strip()

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
