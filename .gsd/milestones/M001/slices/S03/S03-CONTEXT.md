---
id: S03
milestone: M001
status: draft
---

# S03: Parser And Conversion Pipeline — Context

## Goal

Provide a robust background ingestion pipeline that converts CAD documents into engineering graphs with live SSE progress tracking and graceful handling of partial parsing results.

## Why this Slice

This slice establishes the core document understanding capability. It bridges the foundational graph storage (S02) and prepares the structured data needed for subsequent compliance, engineering, and reporting slices, while ensuring the UI remains responsive during long-running conversions.

## Scope

### In Scope

- Executing long-running CAD-to-graph conversions as background tasks.
- Streaming real-time pipeline status (conversion, parsing) to the frontend via SSE.
- Displaying "Processing" and "Ready (Warnings)" states in the FileTree and FilePreview.
- Accepting partial parsing results while surfacing skipped unsupported entities to the user.
- Implementing automatic drawing type detection (`AUTO`) with a post-upload manual override to trigger re-parsing.

### Out of Scope

- Strict rejection of files due to minor parsing warnings.
- Requiring upfront manual classification of drawing types before upload.
- Synchronous blocking of the UI during file conversion.

## Constraints

- Must rely on existing `EngineeringConverter` and `DrawingParserAdapter` contracts without breaking them.
- Must emit SSE events compatible with the frontend's file tree and upload state management.

## Integration Points

### Consumes

- `backend/app/services/engineering_converters.py` — File conversion capabilities.
- `backend/app/services/drawing_parsers.py` — Graph extraction capabilities.

### Produces

- `EngineeringGraph` — The successfully parsed (or partially parsed) graph stored into the knowledge base.
- SSE Event Stream — Live pipeline updates consumed by the frontend FileTree.

## Open Questions

- None at this time.
