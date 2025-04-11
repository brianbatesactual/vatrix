# Streaming Ingestion Pipeline

## Feature
Continuously processes logs from standard input and routes them through the NLP and vectorization pipeline in real time.

## Purpose
- Enable real-time ingestion of SAP audit logs
- Allow users to stream NDJSON input directly into the vector store
- Serve as the primary mode for production log processing

## How It Works

1. `process_stream()` listens to `stdin` via `read_from_stdin()`.
2. Each log entry is parsed as JSON and passed to `process_api_ingest()`.
3. Inside `process_api_ingest`:
   - Deduplication is performed
   - Context is built from raw log
   - Template is matched and rendered
   - Sentence is embedded
   - Vector + metadata is sent to Vatrix-Gateway
   - Sentence is saved via `RotatingStreamWriter`

## Design Choices
- Designed to run as a continuous service (Ctrl+D to end)
- Template matching is required before vector generation
- Each sentence is immediately embedded and upserted
- Local file output is rotated and persisted for audit/logging

## Limitations
- Stream currently assumes stdin input — no Kafka or file tailing
- No retry or backpressure logic in gateway writer
- Deduplication is in-memory only (not persistent)

## Future Work
- Add support for HTTP streaming ingest
- Make process_api_ingest mode-agnostic (batch, stream, realtime)
- Build pipeline stats or event tracing hooks

## Related Modules
stream_runner.py
process_api_ingest.py
stream_reader.py
