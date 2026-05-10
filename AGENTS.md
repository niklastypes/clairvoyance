# Project: Clairvoyance

> A Discord bot that joins voice channels, records sessions, transcribes audio with speaker diarization, and generates AI-powered D&D session summaries.

______________________________________________________________________

## Vision

A bot that serves as an ever-attentive witness to tabletop RPG sessions held over Discord. It silently listens, transcribes everything said, and transforms the raw recording into organized documentation: a searchable transcript, a narrative summary, character development notes, lore discoveries, and scene imagery. The bot operates locally on your own hardware, with optional cloud LLM fallbacks for summarization.

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

- All core features run locally on your own hardware (Whisper, pyannote-audio)
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

### Development Methodology

Based on Henrik Kniberg's [MVP blog post](https://blog.crisp.se/2016/01/25/henrikkniberg/making-sense-of-mvp), we follow an iterative approach where:

- **Each iteration is independently usable** (not useless partial pieces like a car tire)
- **Each iteration provides learning** to inform the next step
- **We deliver early** to get real feedback from users
- **We stay flexible** - the final product may differ from the original vision

The key question for each phase: *What is the cheapest and fastest way we can start learning?*

### Test-Driven Development (TDD)

We practice TDD with the red-green-refactor cycle:

1. **Red** — Write a failing test that describes the desired behavior
2. **Green** — Write minimal code to make the test pass
3. **Refactor** — Clean up code while keeping tests green

Rules:
- Never introduce new functionality without a failing test first
- Tests are first-class citizens, not an afterthought
- Keep tests focused, readable, and fast
- Use `Polyfactory` to generate realistic test data

### Roadmap (Kniberg-style Progression)

| Phase   | Name        | Deliverable                      | User Value          | Learning Goal                      |
| ------- | ----------- | -------------------------------- | ------------------- | ---------------------------------- |
| **MVP** | Bus Ticket  | Bot responds to `!hello` command | Proof bot works     | Discord API auth, command handling |
| **+1**  | Skateboard  | Voice join/leave commands        | Bot joins VC        | Discord voice connections          |
| **+2**  | Scooter     | Audio recording to files         | Session captured    | Audio capture per user             |
| **+3**  | Bicycle     | Basic transcription (.txt)       | Searchable text     | Whisper integration                |
| **+4**  | Motorcycle  | Full transcript (.md + speakers) | Diarized transcript | pyannote diarization               |
| **+5**  | Car         | AI summaries & D&D features      | Narrative summary   | LLM integration                    |
| **+6**  | Convertible | Full feature set                 | Complete experience | Google Docs, scene generation      |

**Note**: We may discover better paths along the way. The "car" we end up with may differ from the original vision based on real user feedback.

______________________________________________________________________

## Coding Principles

### Style & Tooling

- **Packaging**: `uv`
- **Formatting/Linting**: `ruff`
- **Type Checking**: `ty`
- **Data Validation**: `Pydantic` (preferred for all data models, config, API schemas)
- **CLI**: `typer`
- **Testing**: `pytest` + `pytest-bdd`
- **Test Fixtures**: `Polyfactory` (generate realistic test data)
- **Documentation**: `docs/architecture.md` (keep up-to-date with latest changes)

### Code Patterns

- Data models: Use `Pydantic` for all data structures (config, API schemas, domain models)
- Prefer `dataclass` only for trivial internal objects; otherwise, reach for Pydantic
- Functional programming: pure functions, immutability, composition over inheritance
- Avoid side effects where practical
- Type hints: consistent and thorough throughout
- No placeholder types (`Any`, `# type: ignore`)
- Use Python f-strings for logging and print statements (e.g., `logger.info(f"...{var}")` not `logger.info("...%s", var)`)

### Version Control

- Atomic commits
- Conventional commit messages
- Small, focused changes per commit

______________________________________________________________________

## Current State

**Phase 0**: Project initialization ✅
**Phase MVP**: Bot responds to `!hello` command ✅
**Phase +1 (Skateboard)**: Voice join/leave commands ✅

- [x] Repository created
- [x] MVP methodology & roadmap documented
- [x] Discord bot client with config validation
- [x] `!hello` command handler with tests
- [x] CLI entry point (`clairvoyance` command)
- [x] `!join` command — bot joins author's voice channel
- [x] `!leave` command — bot disconnects from voice channel
- [x] Voice state intent enabled
- [x] Tests for voice commands

**Pending user action**:

- [ ] Create Discord bot account and obtain token
- [ ] Set `DISCORD_BOT_TOKEN` environment variable

**Upcoming**: Phase +2 (Scooter) — Audio recording to files
