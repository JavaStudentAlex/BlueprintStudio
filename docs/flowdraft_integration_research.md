# FlowDraft Integration Research

## Source

Repository: `https://github.com/z1nare/flowdraft`

Inspected on 2026-06-07 through GitHub API and raw file access. Rechecked live
on 2026-06-07 before creating this planning surface. Rechecked again on
2026-06-07 after the upstream demo refresh. Repository metadata reported:

- default branch: `main`
- primary language: Python
- description: "Placeholder for the project"
- created: 2026-06-05
- last pushed: 2026-06-07T04:13:35Z
- public repository
- latest reviewed commit: `27f2b509afe8af0068e8995b96e56deb88f9f6fc`
  (`Golden path hackathon demo: guided UI, config reorg, frozen assets`)

Primary upstream files to recheck before implementation:

- `https://github.com/z1nare/flowdraft`
- `https://github.com/z1nare/flowdraft/blob/main/README.md`
- `https://github.com/z1nare/flowdraft/blob/main/docs/REPOSITORY_GUIDE.md`
- `https://github.com/z1nare/flowdraft/blob/main/ArchDraft_Build_Plan.md`
- `https://github.com/z1nare/flowdraft/blob/main/FlowDraft_Build_Plan.md`
- `https://github.com/z1nare/flowdraft/blob/main/schemas/graph.schema.json`
- `https://github.com/z1nare/flowdraft/blob/main/config/bec_rules.yaml`
- `https://github.com/z1nare/flowdraft/blob/main/config/class_map.yaml`
- `https://github.com/z1nare/flowdraft/blob/main/scripts/infer.py`
- `https://github.com/z1nare/flowdraft/blob/main/src/api.py`
- `https://github.com/z1nare/flowdraft/blob/main/src/fusion.py`
- `https://github.com/z1nare/flowdraft/blob/main/src/pue.py`
- `https://github.com/z1nare/flowdraft/blob/main/src/loads.py`
- `https://github.com/z1nare/flowdraft/blob/main/src/finance.py`
- `https://github.com/z1nare/flowdraft/blob/main/data/demo_floorplan.json`
- `https://github.com/z1nare/flowdraft/blob/main/data/demo_compliance_report.json`
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
7. The golden demo pattern: offline `Load demo`, room breakdown, valuation,
   compliance findings, and a precomputed overlay for stage-safe demos.

The least suitable parts to copy directly are:

- static frontend files, because BlueprintStudio already has a Next.js app
- ad hoc secret lookup from files such as `models/secretapi.txt`
- large model weights, source images, and generated overlays
- hackathon-specific file structure and Windows-oriented run commands

## Repository Surface

Key root files:

- `README.md`: quick start, API surface, inference CLI, demo strategy, project
  layout.
- `ArchDraft_Build_Plan.md`: merged architecture plus FlowDraft demo plan.
- `FlowDraft_Build_Plan.md`: detailed hackathon plan for P&ID/SLD parsing,
  3D, compliance, ROI, and Hong Kong data sources.
- `docs/REPOSITORY_GUIDE.md`: current file inventory and keep/delete guide
  after the demo refactor.
- `schemas/graph.schema.json`: canonical graph schema.
- `tests/fixtures/mock_graph.json`, `data/demo_datacentre.json`,
  `data/demo_floorplan.json`, and `data/demo_compliance_report.json`: useful
  graph and compliance fixtures.
- `config/bec_rules.yaml`: small deterministic compliance threshold file.
- `config/class_map.yaml`: YOLO/P&ID class mapping to engineering equipment
  types.
- `config/property_prices/`: Hong Kong property price and rent source tables.
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
- `GET /demo/floorplan`
- `GET /demo/compliance-graph`
- `GET /demo/compliance-report`
- `POST /overlay`
- `POST /compliance/init-demo`
- `GET /compliance/pue`
- `POST /compliance/extract`
- `POST /compliance/rules`
- `GET /compliance/rules`
- `POST /compliance/validate`
- `POST /loads`
- `POST /whatif`
- `GET /finance/districts`
- `POST /finance/property`
- `POST /finance/roi`

BlueprintStudio already has a FastAPI backend, so these should become backend
services/routes under the existing `backend/app` structure rather than a second
standalone API.

## Latest Demo Refresh

Two late upstream commits matter for BlueprintStudio:

- `043f9e2c509c3e85829da4c86fe138db8e427326`: added the TIA-942 compliance
  checker package, SQLite-backed rule persistence, property valuation API/UI,
  data-centre parse routing, and an end-to-end API pipeline script.
- `27f2b509afe8af0068e8995b96e56deb88f9f6fc`: added the golden demo path,
  reorganized config under `config/`, moved tests under `tests/`, removed the
  legacy `whole/` snapshot, added frozen floor-plan and compliance JSON, added
  static demo overlay/source images, and changed the UI around `Load demo`,
  Overlay, Rooms, Valuation, and Compliance tabs.

Coverage in the current BlueprintStudio plan:

- Already covered or implemented: graph schema, FlowDraft fixtures, graph
  validation, fusion service, parser adapter contract, compliance rule model,
  deterministic compliance runner, standards catalog, hybrid retriever,
  electrical load checks, ROI/cost tasks, and frontend graph/compliance tasks.
- Partially covered: PUE/BEC checks, property dataset ingestion, valuation, and
  compliance UI.
- Newly added to the task queue after this recheck: sanitized golden demo
  fixtures, demo/overlay backend surfaces, graph-derived property valuation,
  frontend `Load demo` golden path, and an end-to-end demo smoke test.

Do not copy the upstream static UI wholesale. Translate the behavior into the
existing Next.js shell and keep the demo path deterministic, local, and usable
without API keys.

## CrashPine BlueprintStudio Recheck

Repository: `https://github.com/CrashPine/BlueprintStudio`

Rechecked on 2026-06-07 through local git remotes and GitHub metadata.
Repository metadata reported:

- default branch: `master`
- latest repository push: 2026-06-07T09:56:16Z
- upstream `master`: `df48521fa0def8a58c377827c53966acca642e9c`
- upstream `main`: `a912ae4085c9f03876ac6fd439bfdf12d51f4703`

Comparison against this repo's `origin/main` at recheck time:

- `origin/main...upstream/master`: current repo was 44 commits ahead and
  CrashPine `master` was 3 commits ahead.
- `origin/main...upstream/main`: current repo was 44 commits ahead and
  CrashPine `main` was 3 commits ahead.

The CrashPine-only commits across `master` and `main` were:

- `b550f8f`: replaced the project tree with a standalone FlowDraft hackathon
  submission.
- `df48521`: edited `HONESTY.md` on the default `master` branch.
- `70dc887`: completed `HONESTY.md` with verified working/mocked disclosures
  on `main`.
- `a912ae4`: documented Docker Hub pull path for jurors and added
  `scripts/publish_docker.ps1` on `main`.

Important: `b550f8f` is not safe to merge into this repository. It deletes the
existing BlueprintStudio backend, frontend, tests, and planning surface, then
replaces them with a standalone static/FastAPI FlowDraft demo app. Treat it as
an external implementation reference, not as a branch to merge.

Useful upstream ideas not fully represented before this recheck:

- Root `HONESTY.md` that states what is fully working, partially working,
  mocked, hardcoded, externally dependent, pre-existing, and known-limited.
- Juror/demo Docker packaging: prebuilt image path, `docker compose pull`,
  fallback build, health check, optional profiles, and a scripted demo flow.
- `static/twin.html`: graph-to-3D building twin that extrudes `spaces[]`,
  renders fixtures and MEP nodes/edges, reads the latest parsed graph from
  browser state, and falls back to a demo graph.
- `static/roadmap.html`: capability map that separates live, beta, and roadmap
  features, including an illustrative what-if ROI calculator and CSDI/IoT
  roadmap cards.

Recommended BlueprintStudio response:

- Keep the current Next.js + FastAPI + MemoryPalace application as the product
  base.
- Add an honest capability disclosure document tailored to BlueprintStudio.
- Add demo Docker/runbook tasks only after the offline demo path is stable.
- Add a graph-to-3D twin as a frontend route or view that consumes the canonical
  graph contract.
- Add a capability roadmap page only if it clearly labels live, beta, and
  roadmap items.
- Do not import upstream `models/yolov8n_pid.pt`, raw drawings, overlay PNGs,
  or generated scratch data.

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
estate-level price/rent datasets. The latest repo keeps text data under
`config/property_prices/`.

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
- generated overlay images unless a human explicitly approves a small demo
  asset import
- raw source drawings copied from the external repo
- customer drawings
- API keys in model files
- hackathon-only CSDI/Hong Kong assumptions as global product defaults

Make parser engines optional and test them with fixtures.

## Recommended Integration Order

1. Record the exact upstream FlowDraft commit before each integration batch.
2. Define BlueprintStudio graph schema.
3. Import sanitized FlowDraft demo graphs as fixtures.
4. Add backend graph validation.
5. Port fusion as a typed backend service.
6. Port deterministic PUE/load logic behind tests.
7. Port compliance rule model from `dc_compliance_checker`.
8. Add parser-adapter contracts before importing YOLO/Claude engines.
9. Add golden demo surfaces: local fixtures, overlay rendering, rooms,
   valuation, compliance findings, and e2e smoke tests.
10. Add frontend graph inspection and compliance evidence UI.
11. Add architecture and electrical 2D editor MVPs.
12. Add property/cost datasets and agent RAG workflows.
