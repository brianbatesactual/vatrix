# Template Loader

## Feature
Load the mapping of log categories to template filenames.

## Purpose
- Establish the template to use for each incoming log type
- Enable category-specific rendering

## How It Works
- Loads a YAML or JSON mapping from disk
- Returns a dictionary

## Design Choices
- Keeps template config simple and editable
- Used by both stream and batch modes

## Limitations
- Must be manually kept in sync with available templates
- No default fallback logic in loader

## Related Modules

