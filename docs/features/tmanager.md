# Template Manager

## Feature
Manages Jinja template rendering, including variation selection and error handling.

## Purpose
- Dynamically render logs using category-specific sentence templates
- Support multiple variations per category for data augmentation

## How It Works
- Accepts template name + context
- Selects a `.j2` file (random or fixed mode)
- Renders using `Jinja2`, returns sentence string

## Design Choices
- Allows multiple variations per log type (`variation_1.j2`, `variation_2.j2`, etc.)
- Logs failures with context for debugging
- Random selection helps build robust training sets

## Limitations
- Variation strategy is random — no weighted or deterministic support
- Jinja rendering errors are logged, not raised

## Related Modules

