"""Test factories for Clairvoyance models."""

from __future__ import annotations

from polyfactory.factories.pydantic_factory import ModelFactory

from clairvoyance.bot.client import BotConfig
from clairvoyance.config import Config


class ConfigFactory(ModelFactory[Config]):
    """Factory for creating Config instances for testing."""

    __model__ = Config


class BotConfigFactory(ModelFactory[BotConfig]):
    """Factory for creating BotConfig instances for testing."""

    __model__ = BotConfig
    command_prefix: str = "!"
    activity: str = "D&D sessions"
