"""Tests package initialization."""

from clairvoyance import __version__


def test_version_is_set() -> None:
    """Test that version is properly defined."""
    assert __version__ == "0.1.0"
