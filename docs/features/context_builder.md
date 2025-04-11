# Context Builder

## Feature
Transforms raw SAP log fields into a flat Jinja context dictionary.

## Purpose
- Support safe template rendering
- Ensure all expected template variables are available
- Provide sensible defaults for missing fields

## How It Works
- Accepts a raw `log_entry` dictionary
- Converts keys to lowercase, formats dates, and inserts `na` for blanks
- Returns a fully hydrated dictionary for use in `.j2` templates

## Design Choices
- Avoids mutating the original log
- Provides fallback logic for optional template fields

## Limitations
- Only supports flat log structures
- No nested key resolution

## Related Modules

