# 🔮 Clairvoyance

*Cast [Clairvoyance](https://www.dndbeyond.com/spells/2028-clairvoyance) to create an invisible magical sensor within a Discord voice channel that listens to adventurers and chronicles their tales.*

Discord bot that records D&D/RPG sessions, transcribes them with speaker diarization, and generates AI-powered session summaries.

## Features

- Voice channel recording with per-user audio streams
- Local transcription using Whisper (CPU)
- Speaker diarization with pyannote-audio
- Timestamped markdown transcripts
- AI-powered session summaries (future)

## Quick Start

### 1. Create a Discord Bot

1. Go to [Discord Developer Portal](https://discord.com/developers/applications)
2. Click **New Application** and name it (e.g., "Clairvoyance")
3. In the left sidebar, click **Bot**
4. Click **Reset Token** and copy your bot token (keep it secret!)
5. Under **Privileged Gateway Intents**, enable:
   - ✅ **Message Content Intent** (required for commands)

### 2. Invite the Bot to Your Server

> ⚠️ **Important:** Make sure to select BOTH scopes below. If only `applications.commands` is selected, the bot will not be added to your server!

1. Go to **Installation** in the left sidebar
2. In the **Default Install Settings**, select **BOTH** scopes for **Guild Install**:
   - ✅ `bot` ← **Required!** (don't skip this one)
   - ✅ `applications.commands`
3. For **Permissions**, select:
   - ✅ **Send Messages** (required for bot to reply)
   - ✅ **Read Message History** (required for bot to see messages)
   - ✅ **Connect** (for voice - future)
   - ✅ **Speak** (for voice - future)
4. Copy the **Discord Provided Link** under **Install Link** and paste it in your browser
5. Select your Discord server and click **Authorize**

#### Troubleshooting Invite Issues

If the bot doesn't appear in your server:

- Make sure **Public Bot** is ON in Bot settings
- Make sure **Guild Install** is selected in Installation settings
- Ensure you selected **both** `bot` and `applications.commands` scopes
- Remove and re-invite the bot if needed

### 3. Run the Bot

```bash
# Copy the example env file and add your token
cp .env.example .env

# Edit .env and add your bot token
# DISCORD_BOT_TOKEN=your_bot_token_here

# Run the bot
uv run clairvoyance
```

### 4. Test the Bot

In any Discord text channel the bot can access, use:

| Command               | Description                    |
| --------------------- | ------------------------------ |
| `@Clairvoyance hello` | Check if the bot is responsive |
| `@Clairvoyance join`  | Bot joins your voice channel   |
| `@Clairvoyance leave` | Bot leaves the voice channel   |

Or without mentioning:

| Command | Description                    |
| ------- | ------------------------------ |
| `hello` | Check if the bot is responsive |
| `join`  | Bot joins your voice channel   |
| `leave` | Bot leaves the voice channel   |

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
