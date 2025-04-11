# Deduplication

## Feature
Avoid ingesting duplicate log events during stream processing.

## Purpose
Improve ingestion efficiency by:
- Preventing redundant vector generation
- Reducing noise in semantic search
- Maintaining integrity of the training dataset

## How It Works
`UniqueLogCollector` caches previously seen log entries and returns `False` on duplicates.

Internally uses in-memory hash tracking.

## Design Choices
- Chose in-memory cache for performance
- Simplicity prioritized over persistence for initial implementation

## Limitations
- Not persistent across restarts
- May not scale to multi-process environments

## Future Work
- Use Redis or file-backed caching
- Add TTL-based cache eviction
- Support hash strategy override

## Related Modules
- [`vatrix.pipeline.process_api_ingest`](../../features/stream_pipeline)
- [`vatrix.pipeline.unique_log_collector`](../../features/dedup)
