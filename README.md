# 🔮 Clairvoyance

*Cast to create an invisible magical sensor within a Discord voice channel that listens to adventurers and chronicles their tales.*

Discord bot that records D&D/RPG sessions, transcribes them with speaker diarization, and generates AI-powered session summaries.

## Features

- Voice channel recording with per-user audio streams
- Local transcription using Whisper (CPU)
- Speaker diarization with pyannote-audio
- Timestamped markdown transcripts
- AI-powered session summaries (future)

## Development

### Prerequisites

- Python 3.13+
- [uv](https://github.com/astral-sh/uv) package manager

### Setup

```bash
# Install dependencies
uv sync

# Install development dependencies
uv sync --extra dev

# Install pre-commit hooks
uv run pre-commit install --install-hooks
```

### Pre-commit Hooks

This project uses pre-commit hooks for code quality:

```bash
# Run all hooks manually
uv run pre-commit run --all-files

# Update hook versions
uv run pre-commit auto-update
```

Hooks include:

- Conventional commit validation
- Ruff linting and formatting
- MyPy type checking
- Markdown formatting

### Running Tests

```bash
# Run all tests
uv run pytest

# Run with coverage
uv run pytest --cov=src/clairvoyance
```

### Type Checking

```bash
uv run mypy src/
```

### Linting

```bash
# Check
uv run ruff check src/

# Format
uv run ruff format src/
```

## Versioning

This project uses [Commitizen](https://commitizen-tools.github.io/commitizen/) with conventional commits:

```bash
# Check current version
uv run cz version

# Bump version (creates commit and tag)
uv run cz bump

# Dry run
uv run cz bump --dry-run
```

## Docker

```bash
# Build image
docker build -t clairvoyance .

# Run with docker-compose
docker compose up
```

## License

MIT

---

Built with ❤️ using uv, discord.py, and Whisper.
