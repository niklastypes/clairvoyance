# Architecture

> Keep this file up-to-date with the latest implementation changes.

______________________________________________________________________

## Current State (Phase +1: Skateboard)

```mermaid
graph TD
    subgraph Discord["Discord"]
        API["Discord API"]
        TextMsg["Text Message"]
        VoiceChannel["Voice Channel"]
    end

    subgraph Bot["Bot"]
        Client["discord.py Client"]
        subgraph Commands["Commands"]
            Hello["handle_hello()<br/>!hello"]
            Join["handle_join()<br/>!join"]
            Leave["handle_leave()<br/>!leave"]
        end
    end

    API -->|"on_message"| Client
    Client --> Hello
    Client --> Join
    Client --> Leave
    Join -->|"connect()"| VoiceVC["Voice Client"]
    Leave -->|"disconnect()"| VoiceVC

    TextMsg -->|"reply()"| API
    VoiceChannel -->|"audio"| VoiceVC
```

### Concepts

| Concept        | Responsibility                                       |
| -------------- | ---------------------------------------------------- |
| `Bot`          | Manages Discord connection, intents, message routing |
| `Config`       | Loads environment config (`DISCORD_BOT_TOKEN`)       |
| `handle_hello` | Responds with greeting                               |
| `handle_join`  | Connects to user's voice channel                     |
| `handle_leave` | Disconnects from voice channel                       |

______________________________________________________________________

## Planned 🗓

```mermaid
graph TD
    subgraph Discord["Discord"]
        Channel["Voice Channel"]
        Messages["Text Messages"]
    end

    subgraph Players["Players"]
        User1["Player A"]
        User2["Player B"]
        DM["Dungeon Master"]
    end

    subgraph Bot["Bot"]
        VC["Voice Connection"]
        Recorder["Session Recorder"]
        Processor["Audio Processor"]
        Transcriber["Whisper + Diarizer"]
        Formatter["Transcript Formatter"]
        Summarizer["Summarizer"]
    end

    subgraph Output["Output"]
        Transcript["📝 Transcript"]
        Summary["📋 Summary"]
    end

    User1 & User2 & DM -->|"voice"| Channel
    Channel -->|"audio stream"| VC
    VC --> Recorder
    Recorder --> Processor
    Processor --> Transcriber
    Transcriber --> Formatter
    Formatter --> Transcript
    Formatter --> Summarizer
    Summarizer --> Summary

    Messages -->|"!start / !stop"| Bot
    Transcript -->|"upload"| Messages
    Summary -->|"post"| Messages
```

### Concepts

| Concept       | Responsibility           | Phase |
| ------------- | ------------------------ | ----- |
| `Recorder`    | Capture audio per user   | +2    |
| `Processor`   | Merge, normalize audio   | +2    |
| `Transcriber` | Whisper for STT          | +3    |
| `Diarizer`    | pyannote for speaker IDs | +4    |
| `Formatter`   | Markdown with timestamps | +4    |
| `Summarizer`  | LLM for session summary  | +5    |

______________________________________________________________________

*Last updated: +1 (Skateboard)*
