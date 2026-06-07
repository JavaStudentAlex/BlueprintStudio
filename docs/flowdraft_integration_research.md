# FlowDraft Integration Research

## Source

Repository: `https://github.com/z1nare/flowdraft`

Inspected on 2026-06-07 through GitHub API and raw file access. Rechecked live
on 2026-06-07 before creating this planning surface. Repository metadata
reported:

- default branch: `main`
- primary language: Python
- description: "Placeholder for the project"
- created: 2026-06-05
- last pushed: 2026-06-07
- public repository

Primary upstream files to recheck before implementation:

- `https://github.com/z1nare/flowdraft`
- `https://github.com/z1nare/flowdraft/blob/main/README.md`
- `https://github.com/z1nare/flowdraft/blob/main/ArchDraft_Build_Plan.md`
- `https://github.com/z1nare/flowdraft/blob/main/FlowDraft_Build_Plan.md`
- `https://github.com/z1nare/flowdraft/blob/main/schemas/graph.schema.json`
- `https://github.com/z1nare/flowdraft/blob/main/scripts/infer.py`
- `https://github.com/z1nare/flowdraft/blob/main/src/api.py`
- `https://github.com/z1nare/flowdraft/blob/main/src/fusion.py`
- `https://github.com/z1nare/flowdraft/blob/main/src/pue.py`
- `https://github.com/z1nare/flowdraft/blob/main/src/loads.py`
- `https://github.com/z1nare/flowdraft/blob/main/src/finance.py`
- `https://github.com/z1nare/flowdraft/blob/main/docs/VIEWER_SPEC.md`
- `https://github.com/z1nare/flowdraft/blob/main/docs/DEMO_SCENARIOS.md`

## Executive Summary

FlowDraft is a hackathon-style prototype that combines architectural floor-plan
parsing with MEP parsing for P&ID, HVAC, SLD, data-centre layouts, PUE/BEC
checks, electrical load checks, ROI, and a simple static UI.

The most valuable integration targets for BlueprintStudio are:

1. The unified graph schema.
2. Parser routing across floor plan, PID, SLD, and data-centre diagram types.
3. Fusion of architectural spaces with MEP equipment through `space_id`.
4. Deterministic engineering checks: PUE, BEC, loads, breaker headroom, ROI.
5. Demo datasets and graph fixtures for tests.
6. Viewer behavior specification for graph-to-3D and later 2D/3D UI.

The least suitable parts to copy directly are:

- static frontend files, because BlueprintStudio already has a Next.js app
- ad hoc secret lookup from files such as `models/secretapi.txt`
- large model weights and generated overlays
- hackathon-specific file structure and Windows-oriented run commands

## Repository Surface

Key root files:

- `README.md`: quick start, API surface, inference CLI, demo strategy, project
  layout.
- `ArchDraft_Build_Plan.md`: merged architecture plus FlowDraft demo plan.
- `FlowDraft_Build_Plan.md`: detailed hackathon plan for P&ID/SLD parsing,
  3D, compliance, ROI, and Hong Kong data sources.
- `schemas/graph.schema.json`: canonical graph schema.
- `mock_graph.json` and `data/demo_datacentre.json`: useful graph fixtures.
- `bec_rules.yaml`: small deterministic compliance threshold file.
- `class_map.yaml`: YOLO/P&ID class mapping to engineering equipment types.
- `scripts/infer.py`: production inference CLI.
- `src/api.py`: FastAPI endpoints.
- `src/fusion.py`: graph fusion and routing.
- `src/pue.py`: PUE and BEC checks.
- `src/loads.py`: electrical load analysis.
- `src/finance.py`: property and ROI estimation.

## API Capabilities

`src/api.py` exposes these useful endpoints:

- `GET /health`
- `POST /parse`
- `POST /fuse`
- `GET /schema`
- `GET /demo-graph`
- `GET /demo-datacentre`
- `GET /compliance/pue`
- `POST /loads`
- `POST /whatif`
- `POST /finance/roi`

BlueprintStudio already has a FastAPI backend, so these should become backend
services/routes under the existing `backend/app` structure rather than a second
standalone API.

## Unified Graph Contract

FlowDraft's graph schema supports:

- `meta`: diagram ID, diagram type, building ID, source file, parse confidence,
  parser, warnings, PUE, IT power, facility power, total area, scale, title, and
  drawing metadata.
- `spaces`: rooms with category, polygon, area, dimensions, floor, confidence,
  and optional IT load.
- `walls`: wall polylines.
- `fixtures`: architectural fixtures such as doors, windows, stairs, columns,
  toilets, sinks, and kitchen items.
- `nodes`: equipment, instruments, valves, signals, towers, chillers, pumps,
  transformers, switchgear, breakers, distribution panels, CRAC/CRAH, UPS, PDU,
  busway, and racks.
- `edges`: chilled-water supply/return, condenser water, air ducts, electrical
  cable, control signal, and unknown edges.
- `annotations`: notes, dimensions, tags, scales, and other extracted text.

For BlueprintStudio, this should be generalized into a multi-discipline
building graph that also covers:

- plumbing pipes, drains, fixtures, risers, valves, meters, and pump sets
- ventilation equipment, fans, ducts, diffusers, dampers, and airflow edges
- electrical panels, circuits, outlets, switches, luminaires, routes, loads, and
  protective devices
- compliance rules, source clauses, and violation evidence
- provenance from uploaded files, page numbers, drawing regions, parser engine,
  and confidence

## Parser And Conversion Pipeline

FlowDraft's `scripts/infer.py` is the best integration reference. It routes:

- `FLOORPLAN`
- `PID`
- `SLD`
- `FUSED`
- `DC_DATAHALL`
- `DC_SERVERROOM`
- `COOLING_PID`
- `AUTO`

It supports:

- YOLO weights for P&ID symbols
- Anthropic key for Claude/VLM extraction
- Roboflow key for floor-plan room/fixture detection
- schema validation
- debug mark images
- optional handwriting extraction
- overlay rendering

BlueprintStudio should treat these as optional parser engines. Default tests
must use fixtures and fakes, not live external model calls.

## Fusion Layer

`src/fusion.py` provides a clean starting point:

- `detect_diagram_class`
- `assign_space_ids`
- `fuse_graphs`
- `parse_unified`

The most important behavior is point-in-polygon assignment of MEP node centers
into architectural `spaces`, producing `node.space_id`.

BlueprintStudio should add:

- typed pydantic models
- provenance on every assignment
- validation warnings for unassigned nodes
- conflict handling when a node is near multiple spaces
- persistence of fused graph artefacts per uploaded document or project

## Compliance And Load Engines

`src/pue.py` and `src/loads.py` demonstrate the right split:

- deterministic code computes PUE, BEC, loads, current, and breaker headroom
- LLMs do not decide pass/fail
- YAML rules drive thresholds

Useful calculations:

- `PUE = facility_power_kW / it_power_kW`
- facility power can be derived from IT plus cooling, electrical overhead, and
  modeled equipment
- downstream electrical load is summed by graph traversal
- three-phase breaker current is computed from load, voltage, and power factor
- overload uses a threshold fraction of ampacity

BlueprintStudio should reuse the approach but broaden it:

- electrical discipline checks
- HVAC and ventilation checks
- plumbing topology checks
- standard-specific rule sets
- violation evidence objects
- human-reviewed rules extracted from official sources

## Finance And Property Data

`src/finance.py` estimates property value and ROI from floor area, district, and
estate-level price/rent datasets. The repo includes text data under
`average_property_price/`.

BlueprintStudio should not hardcode these datasets directly into business
logic. Instead, create:

- dataset catalog
- import pipeline
- source provenance
- normalized price/rent/cost tables
- vector-indexed source summaries for agent Q&A
- deterministic calculators for costs and ROI

## Viewer Contract

`docs/VIEWER_SPEC.md` defines the expected scene:

- room slabs from `spaces`
- optional walls
- MEP nodes positioned by `space_id`
- MEP edges as tubes
- labels
- system toggles
- ghost what-if mode
- PUE/compliance panel
- upload flow for floor plan and P&ID/SLD

BlueprintStudio should translate this into its existing Next.js shell:

- graph view for canonical graph inspection
- report view for compliance evidence
- future 2D editor for architecture and electrical layers
- optional 3D/digital-twin view after the graph contract stabilizes

## Data And Model Risks

Do not commit or rely on:

- large YOLO `.pt` weights
- generated overlay images
- customer drawings
- API keys in model files
- hackathon-only CSDI/Hong Kong assumptions as global product defaults

Make parser engines optional and test them with fixtures.

## Recommended Integration Order

1. Define BlueprintStudio graph schema.
2. Import FlowDraft demo graph as a fixture.
3. Add backend graph validation.
4. Port fusion as a typed backend service.
5. Port deterministic PUE/load logic behind tests.
6. Port compliance rule model from `dc_compliance_checker`.
7. Add parser-adapter contracts before importing YOLO/Claude engines.
8. Add frontend graph inspection and compliance evidence UI.
9. Add architecture and electrical 2D editor MVPs.
10. Add property/cost datasets and agent RAG workflows.
