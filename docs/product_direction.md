# BlueprintStudio Product Direction

## Purpose

This document defines the product and technical direction for BlueprintStudio.
It turns local research, the `dc_compliance_checker` prototype, the FlowDraft
public repository, and the team's high-level task list into a coherent roadmap.

`agent_tasks.json` is the executable task queue. This document explains why the
queue exists and how new tasks should be generated.

## Product Vision

BlueprintStudio should become a multi-discipline building-engineering agent for
construction documents, engineering drawings, real-estate data, standards, and
cost reasoning.

The target product is not only an architectural-document chat app. It should
support:

- architecture and room geometry
- electrical systems, panels, circuits, loads, and single-line diagrams
- plumbing and pipe networks
- HVAC, cooling, ventilation, air ducts, and equipment schedules
- data-centre and technical-room analysis where useful for demos
- standards and compliance checking, including GOST-oriented workflows
- property and real-estate database retrieval for RAG
- approximate pricing, cost, ROI, and market analysis
- 2D editing for architecture and electrical layouts
- agent-generated reports with evidence, warnings, and candidate fixes

## Source Inputs

The current direction is grounded in these inputs:

- `deep-research-report.md`: database architecture and GraphRAG research.
- `dc_compliance_checker/`: proof-of-concept rule extraction, geometry parsing,
  topology validation, and compliance reporting.
- `https://github.com/z1nare/flowdraft`: external project to fuse into
  BlueprintStudio, especially graph schema, parser router, FlowDraft/ArchDraft
  fusion, PUE/BEC, electrical load checks, ROI, and viewer contract.
- Team task list:
  - YOLO-based conversion.
  - Integration into the current project.
  - Agent development and real-estate databases for vector RAG.
  - Standards checking via official-source scraping and AI-assisted processing.
  - Approximate cost estimation through the agent.
  - 2D editor for architecture.
  - 2D editor for electrification.

## Target Architecture

The research report's strongest recommendation is a hybrid architecture:

```text
uploaded sources
  -> controlled parsers and extractors
  -> authoritative engineering graph
  -> deterministic validation and rule engines
  -> vector/text retrieval for direct clause lookup
  -> GraphRAG for topology and multi-hop reasoning
  -> LLM explanation and candidate-fix generation
  -> human approval for physical or compliance-impacting changes
```

### Source Of Truth

MemoryPalace remains useful for agent memory and document recall, but it should
not become the authoritative engineering database.

The authoritative engineering state should be a graph-oriented model with
explicit schema, provenance, and validation. Early implementation may use
PostgreSQL JSONB and SQLite-backed fixtures, but the target design should keep a
clean path to a property graph or RDF/semantic graph backend.

The recommended long-term store candidates are:

- Neo4j for the fastest GraphRAG and graph-analytics path.
- TuGraph or NebulaGraph when deployment constraints favor that ecosystem or
  very large scale.
- RDF/OWL plus SHACL where standards-grounded semantic validation is critical.

### Hybrid Retrieval

Use different retrieval modes for different questions:

- Vector/text RAG: direct standards clauses, narrow factual lookup, document
  snippets, and report evidence.
- Graph retrieval: topology, connectivity, contradictions, multi-hop equipment
  reasoning, missing links, and impact analysis.
- Deterministic rules: pass/fail compliance checks, load calculations, area
  checks, path safety, and numeric thresholds.
- LLM layer: explanation, report drafting, candidate fixes, and user-facing
  synthesis.

## Engineering Graph Contract

BlueprintStudio needs a canonical graph contract that can represent multiple
disciplines:

- `spaces`: architectural rooms, areas, floors, zones, and room categories.
- `walls` and `fixtures`: architecture and 2D editor geometry.
- `nodes`: equipment, panels, valves, meters, ducts, pipes, fixtures, racks,
  transformers, switchgear, distribution panels, sensors, and discipline
  objects.
- `edges`: pipe, duct, electrical, control, adjacency, containment, supply,
  return, drain, and logical links.
- `annotations`: text, handwritten notes, callouts, dimensions, and provenance.
- `meta`: source file, parser, confidence, building, units, scale, graph
  version, and source validity.

FlowDraft's `schemas/graph.schema.json` is the best immediate starting point,
but it must be extended beyond data-centres into general building disciplines:

- architecture
- electrical
- plumbing
- HVAC
- ventilation
- compliance
- cost and market context

## Compliance Direction

Compliance should follow a gated flow:

```text
official standard source
  -> source catalog
  -> clause extraction
  -> human-reviewed rule normalization
  -> deterministic rule execution
  -> violation evidence
  -> agent explanation
  -> report and candidate fixes
```

The `dc_compliance_checker` prototype already proves several useful concepts:

- `Rule` and `GeometryObject` schemas that bridge text rules and geometry.
- controlled target vocabularies for room, aisle, rack, equipment, and building
  entities.
- numeric conditions such as area, width, clearance, power, and PUE.
- topology conditions such as `must_exist` and `must_connect_to`.
- networkx-based validation over graph links.
- standard-document parsing into machine-checkable rules.
- SQLAlchemy persistence for rules with PostgreSQL and SQLite fallback.

This should be ported into the main backend as a governed compliance service,
not kept as a side project.

## FlowDraft Fusion Direction

FlowDraft contributes the most useful external implementation surface:

- unified graph schema for floor plans, P&ID, SLD, and fused graphs
- parser router for `AUTO`, `FLOORPLAN`, `PID`, `SLD`, and data-centre modes
- YOLO plus Claude hybrid parser paths
- point-in-polygon fusion of MEP nodes into architectural spaces
- deterministic PUE/BEC checks
- electrical load and breaker headroom checks
- property price and ROI estimation from parsed floor area
- 3D viewer specification for graph and room rendering

BlueprintStudio should not blindly copy FlowDraft as a separate app. The correct
direction is to absorb its contracts and stable engines behind existing backend
services and frontend surfaces.

## Demo Direction

The latest FlowDraft demo update is useful because it packages existing
engineering pieces into a short, deterministic product story: load a frozen
floor-plan graph, show labeled rooms and area, estimate property value, run a
compliance check, and show a roadmap from architecture into P&ID, data-centre,
and 3D work.

BlueprintStudio should copy that demo behavior, not the static implementation.
The demo path should:

- run without live API keys, model weights, or third-party calls
- use sanitized graph and compliance fixtures with provenance
- avoid committing large overlay/source images unless explicitly approved
- expose backend demo and overlay surfaces through existing FastAPI modules
- render the workflow inside the existing Next.js shell
- be covered by a deterministic backend/frontend smoke test

## 2D Editor Direction

The 2D editor should be built as an engineering tool, not a decorative canvas.
It must support:

- architecture layers: rooms, walls, openings, labels, dimensions, areas
- electrical layers: panels, circuits, switches, outlets, fixtures, cable paths
- later layers: plumbing, HVAC, ventilation, equipment, and annotations
- graph-backed editing so geometry changes update the canonical graph
- validation overlays for compliance and missing data
- export/import through the same graph contract used by parsers

## Agent Direction

The agent should answer and act through a contract like:

```text
warning
  -> evidence
  -> violated rule or graph condition
  -> confidence and provenance
  -> candidate fixes ranked by feasibility
  -> human approval for write-back
```

The agent should never silently update engineering parameters, compliance
rules, or generated reports without a visible evidence trail and user approval.

## Roadmap Phases

### Phase 0: Governance And Contracts

- Create `agent_tasks.json`, planning docs, and backlog.
- Validate task manifests.
- Define source priority for Jules/Codex.
- Produce FlowDraft integration map.

### Phase 1: Graph Foundation

- Define a BlueprintStudio graph schema.
- Import FlowDraft mock/demo graph fixtures.
- Add backend graph validation and typed models.
- Add provenance and source-span contracts.

### Phase 2: Parser And Conversion Pipeline

- Integrate image/PDF conversion endpoints.
- Add YOLO/P&ID parser adapters as optional engines.
- Add floor-plan parser contract and fixtures.
- Store parser outputs as graph artefacts tied to uploaded documents.

### Phase 3: Compliance And Standards

- Port `dc_compliance_checker` rule model.
- Build standards source catalog.
- Add deterministic compliance runner.
- Add GOST-oriented rule extraction workflow.
- Add violation evidence and report integration.

### Phase 4: Databases And RAG

- Design authoritative graph storage.
- Add real-estate and cost-data ingestion.
- Index approved datasets into vector RAG.
- Add graph/text hybrid retrieval for the agent.

### Phase 5: Multidiscipline Engineering

- Add electrical load topology checks.
- Add plumbing and pipe graph primitives.
- Add HVAC and ventilation primitives.
- Add candidate fix generation based on graph evidence.

### Phase 6: 2D Editing And Review UI

- Add architecture editor MVP.
- Add electrical editor MVP.
- Add MEP layers and compliance overlays.
- Tie edits back to the canonical graph.

### Phase 7: Cost, ROI, And Reporting

- Add approximate price estimation.
- Add material/equipment cost catalog.
- Add ROI and scenario calculations.
- Extend report pipeline to generate engineering and compliance reports.

## Guardrails

- Do not treat the LLM as the source of compliance truth.
- Do not store uploaded construction documents or generated reports outside
  ignored runtime data paths.
- Do not call real external LLMs, standards sites, government sites, or APIs
  from default tests.
- Do not add large YOLO weights or customer drawings to git.
- Do not change GitHub workflow, secret, or auto-merge behavior as part of
  normal feature tasks.
- Keep every autonomous task narrow, testable, and scoped to explicit paths.
