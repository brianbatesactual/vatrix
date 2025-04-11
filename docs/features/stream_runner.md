# Stream Runner

## Feature
Entry point for real-time streaming via CLI. Orchestrates live log ingestion and passes events to `process_api_ingest`.

## Purpose
- Serve as CLI trigger for `make stream`
- Wrap `stdin` reading, rendering, embedding, and gateway forwarding

## How It Works
- Calls `read_from_stdin()` → yields log entries
- For each entry, calls `process_api_ingest()`
- Handles logging, deduplication, and error recovery

## Design Choices
- Small wrapper around stream ingestion logic
- Abstracts mode-specific wiring away from CLI

## Limitations
- Assumes logs are NDJSON formatted
- Does not expose config flags or batch behavior

## Related Modules

