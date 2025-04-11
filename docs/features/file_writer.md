# File Writer

## Feature
Write unmatched or diagnostic logs to a flat JSON file for further analysis.

## Purpose
- Capture logs that don't match any template
- Retain data during pipeline exceptions or mismatches
- Enable offline inspection or training dataset seeding

## How It Works
- Called from `process_api_ingest()` or `process_stream()` when `template_name == default_template.txt`
- Appends JSON entries to a user-defined file

## Design Choices
- JSON format chosen for structure and compatibility
- File path is parameterized (or defaults)
- Writes are immediate and non-batched

## Limitations
- No log rotation or size control
- No batching or async writes

## Related Modules

