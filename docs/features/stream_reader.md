# Stream Reader

## Feature
Reads NDJSON logs from standard input for live ingestion.

## Purpose
- Accept logs from pasted CLI events, file pipes, or stdin redirect
- Serve as input layer for `make stream`

## How It Works
- Blocks on `input()` loop until EOF (Ctrl+D)
- Parses each line as JSON
- Yields valid entries to `process_stream()`

## Design Choices
- Built for CLI and manual debugging scenarios
- Fail-fast for malformed lines

## Limitations
- Only handles `stdin` — no sockets, pipes, or Kafka
- No rate limiting or timeout support

## Related Modules

