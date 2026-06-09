# Phase 2: Parser And Conversion Pipeline

**Vision:** Optional parser engines, YOLO/IFC planning, and graph artifact persistence.

## Slices

- [ ] **S01: Plan YOLO-based drawing conversion integration** `risk:high` `depends:[]`
  > After this: Spike plan defines optional-engine boundaries, fixtures, model-weight policy, and no-default-network tests.

- [ ] **S02: Plan IFC ingestion spike** `risk:high` `depends:[S01]`
  > After this: Spike defines IFC scope, fixtures, graph output, risks, and implementation boundaries.
# Phase 3: Compliance And Standards

**Vision:** Deterministic standards, GOST-oriented ingestion, external-source policy, and evidence contracts.

## Slices

- [ ] **S01: Plan GOST-oriented standards ingestion** `risk:high` `depends:[]`
  > After this: Plan covers source catalog, clause extraction, human review, deterministic rule normalization, and approval gates.

- [ ] **S02: Define external source access policy** `risk:high` `depends:[S01]`
  > After this: Policy defines approval gates for standards sites, government sources, scraping, paid APIs, and live external calls.
# Phase 4: Databases And RAG

**Vision:** Authoritative graph storage path, real-estate data, property RAG fixtures, and hybrid retrieval.

## Slices

- [ ] **S01: Create real-estate dataset catalog** `risk:medium` `depends:[]`
  > After this: Catalog records source, license, geography, update cadence, fields, and suitability for RAG/cost use.

- [ ] **S02: Add property price RAG fixture workflow** `risk:medium` `depends:[S01]`
  > After this: Curated fixture data indexes deterministically with source metadata and test coverage.
# Phase 5: Multidiscipline Engineering

**Vision:** Electrical, plumbing, ventilation, HVAC, candidate fixes, and agent warning workflow.

## Slices

- [ ] **S01: Define ventilation graph taxonomy** `risk:low` `depends:[]`
  > After this: Taxonomy defines fans, AHUs, ducts, dampers, diffusers, zones, airflow edges, provenance, and validation cases.

- [ ] **S02: Add agent warning and candidate fix workflow** `risk:medium` `depends:[S01]`
  > After this: Agent emits warning, evidence, violated condition, confidence, provenance, ranked fixes, and human-approval gate.
# Phase 6: 2D Editing And Review UI

**Vision:** Graph/compliance inspection, graph-to-3D twin, roadmap view, and architecture/electrical editors.

## Slices

- [ ] **S01: Add graph-to-3D twin frontend view** `risk:medium` `depends:[]`
  > After this: View consumes canonical graph fixtures and renders spaces, fixtures, MEP nodes/edges, labels, and fallback state.

- [ ] **S02: Add capability roadmap view** `risk:low` `depends:[S01]`
  > After this: UI labels live, beta, mocked, and roadmap capabilities without overstating implementation status.

- [ ] **S03: Add frontend graph inspection view** `risk:medium` `depends:[S02]`
  > After this: Users can inspect graph objects, relationships, provenance, confidence, and validation warnings.

- [ ] **S04: Add compliance results UI** `risk:medium` `depends:[S03]`
  > After this: UI renders deterministic violations with rule, object, actual, expected, source, confidence, and candidate fixes.

- [ ] **S05: Design architecture 2D editor state model** `risk:medium` `depends:[S04]`
  > After this: Design covers walls, rooms, openings, labels, dimensions, areas, layers, validation, and graph write-back.

- [ ] **S06: Build architecture 2D editor MVP** `risk:medium` `depends:[S05]`
  > After this: MVP supports graph-backed architecture edits and deterministic tests for core interactions.

- [ ] **S07: Design electrical 2D editor state model** `risk:medium` `depends:[S06]`
  > After this: Design covers panels, circuits, switches, outlets, fixtures, cable paths, schedules, and validation.

- [ ] **S08: Build electrical 2D editor MVP** `risk:medium` `depends:[S07]`
  > After this: MVP supports graph-backed electrical edits and deterministic tests for core interactions.
# Phase 7: Cost, ROI, And Reporting

**Vision:** Cost calculators, ROI scenario service, and compliance evidence in report generation.

## Slices

- [ ] **S01: Implement approximate cost estimation service** `risk:medium` `depends:[]`
  > After this: Service computes deterministic cost estimates before LLM explanation and exposes assumptions/provenance.

- [ ] **S02: Add ROI and scenario calculation service** `risk:medium` `depends:[S01]`
  > After this: Service computes scenario ROI from explicit inputs and records assumptions/provenance.

- [ ] **S03: Extend report pipeline with compliance evidence** `risk:medium` `depends:[S02]`
  > After this: Reports include compliance evidence while preserving report-session validation gates and export safety.
# Phase 8: Demo Packaging And Disclosure

**Vision:** Offline golden demo frontend, smoke tests, honesty docs, upstream logs, and runbooks.

## Slices

- [ ] **S01: Add CrashPine upstream recheck log** `risk:low` `depends:[]`
  > After this: Latest reviewed CrashPine branch/commit SHAs are recorded with merge safety notes.

- [ ] **S02: Add demo capability honesty disclosure** `risk:low` `depends:[S01]`
  > After this: Disclosure separates live, beta, mocked, hardcoded, external-service, and roadmap behavior.

- [ ] **S03: Add deterministic demo Docker runbook** `risk:medium` `depends:[S02]`
  > After this: Runbook documents offline demo startup, health checks, fallback build, and no-secret assumptions.
