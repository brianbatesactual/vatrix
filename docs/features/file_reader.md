# File Reader

## Feature
Load logs from newline-delimited JSON (NDJSON) files for batch processing.

## Purpose
- Process historical log archives
- Enable SBERT dataset creation from saved logs
- Support `--mode file` CLI option

## How It Works
- Reads from user-specified NDJSON file path
- Parses each line into a dictionary
- Yields entries to the processor

## Design Choices
- Streaming read line-by-line to handle large files
- Graceful skip on JSON parse errors

## Limitations
- No support for nested folders or compressed files
- No inline filtering or transformation

## Related Modules

