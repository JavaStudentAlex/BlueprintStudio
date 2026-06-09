---
estimated_steps: 16
estimated_files: 2
skills_used: []
---

# T02: Instrument conversion and parser pipeline

---
skills_used:
  - tdd
  - verify-before-complete
---
Why: The existing ingestion service performs conversion, parser, graph artifact, and KB indexing work synchronously without fine-grained progress or partial-warning semantics.

Do:
- Update ingest_registered_files and helper functions to accept an optional ingestion event publisher without breaking existing callers such as ingest_directory.
- Emit deterministic events for queued, processing, conversion_started, conversion_complete, parser_started, parser_complete, indexing_started, indexed, skipped, failed, and warning transitions.
- Preserve existing EngineeringConverter and DrawingParserAdapter protocols; do not require adapter signature changes.
- Treat ParserResult warnings as partial success when the parser returns a usable EngineeringGraph, persist those warnings on the document registry, store the graph artifact, and continue indexing safe converted content.
- Keep converter failures, missing configuration, unsupported extensions, and parser exceptions isolated per document so one failed file does not abort the batch.

Done when:
- Fake converter and fake parser tests prove successful conversion, skipped conversion, failed conversion, parser warning partial success, parser exception failure, duplicate-upload short circuit, and graph artifact storage behavior.
- Q5: Per-file failure modes are tested and do not crash the batch.
- Q7: Negative tests cover parser exception, converter missing output, and unsupported extension.

## Inputs

- `backend/app/services/ingestion.py`
- `backend/app/services/engineering_converters.py`
- `backend/app/services/drawing_parsers.py`
- `backend/app/services/graph_artifacts.py`
- `backend/app/services/ingest_events.py`
- `backend/tests/unit/test_ingestion.py`

## Expected Output

- `backend/app/services/ingestion.py`
- `backend/tests/unit/test_ingestion.py`

## Verification

rtk uv --directory backend run --extra dev pytest tests/unit/test_ingestion.py tests/unit/test_ingest_events.py

## Observability Impact

Adds stage-level backend progress emission and warning/error state transitions for conversion, parser, graph artifact, and indexing work.
