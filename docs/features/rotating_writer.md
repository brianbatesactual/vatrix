# Rotating Stream Writer

## Feature
Automatically rotates local file output for streamed rendered logs.

## Purpose
- Persist generated sentences from the stream pipeline
- Avoid unbounded file growth
- Segment logs by time

## How It Works
- Rotates files by date (`streamed_logs_YYYYMMDD_HHMMSS.csv`)
- Appends each rendered sentence on a new line
- Automatically creates target directory if missing

## Design Choices
- Named file using timestamp to avoid overwrite
- Streamed logs written in CSV format for readability and ingestion
- Writer initialized once per run

## Limitations
- No file size-based rotation yet
- Doesn't delete or clean up old logs

## Related Modules

