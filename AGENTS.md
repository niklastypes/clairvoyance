# Project: Clairvoyance

> A Discord bot that joins voice channels, records sessions, transcribes audio with speaker diarization, and generates AI-powered D&D session summaries.

______________________________________________________________________

## Vision

A bot that serves as an ever-attentive witness to tabletop RPG sessions held over Discord. It silently listens, transcribes everything said, and transforms the raw recording into organized documentation: a searchable transcript, a narrative summary, character development notes, lore discoveries, and scene imagery. The bot operates locally on a Mac Mini M4, with optional cloud LLM fallbacks for summarization.

______________________________________________________________________

## Core Use Case

D&D session documentation:

- Record voice channel sessions (post-session processing, not real-time)
- Transcribe with accurate speaker identification
- Generate markdown transcripts with timestamps
- Produce AI-powered D&D session summaries with:
  - Session narrative arc
  - Character development tracking
  - Lore & world-building notes
  - Scene clustering for potential image generation
- Optional Google Docs integration for shared storage

______________________________________________________________________

## Technical Principles

### Local-First, Cloud-Optional

- All core features run locally on the Mac Mini (Whisper, pyannote-audio)
- Cloud services (LLM APIs, Google Docs) are opt-in extensions
- Architecture must not depend on external services to function

### CI/CD

- GitHub Actions for QA checks (pre-commit, type-check, lint, test, docker-build)
- Semantic versioning via Commitizen with conventional commits
- Automated releases on version tags

### Version Bumping

- Use `uv run cz bump` to bump version based on conventional commits
- Or trigger `bump-version` workflow manually in GitHub Actions

### Recording & Processing Flow

1. Bot joins voice channel on user command
2. Records each participant's audio stream individually
3. Session ends when channel empties or via manual command
4. Audio files processed through transcription pipeline
5. Output: .md transcript with speaker labels
6. Optional: upload to Google Docs, post notification to Discord

______________________________________________________________________

## Coding Principles

### Style & Tooling

- **Packaging**: `uv`
- **Formatting/Linting**: `ruff`
- **Type Checking**: `ty`
- **Type Models**: `Pydantic`
- **CLI**: `typer`
- **Testing**: `pytest` + `pytest-bdd`

### Code Patterns

- Functional programming: pure functions, immutability, composition over inheritance
- Avoid side effects where practical
- Type hints: consistent and thorough throughout
- No placeholder types (`Any`, `# type: ignore`)

### Version Control

- Atomic commits
- Conventional commit messages
- Small, focused changes per commit

______________________________________________________________________

## Current State

**Phase 0**: Project initialization

- [x] Repository created
- [ ] Discord bot account setup (pending user action)
- [ ] Environment configuration

**Upcoming**: Phase 1 — Bot foundation with voice join/leave commands
