# Processor (Batch Mode)

## Feature
Run batch processing of logs from file, including rendering, scoring, and dataset export.

## Purpose
- Transform a full log archive into:
  - Rendered sentences
  - SBERT sentence pairs
  - Scored similarity data

## How It Works
- Reads NDJSON log input
- Matches each log to a template
- Renders sentence
- Optionally generates SBERT sentence pairs and cosine similarity scores

## Design Choices
- Central command layer for `--mode file`
- Modular: rendering, scoring, and exporting are plug-in calls

## Limitations
- Requires templates to be pre-loaded
- No streaming or incremental modes here

## Related Modules

