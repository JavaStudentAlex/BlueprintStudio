# Roadmap: BlueprintStudio

## Overview

BlueprintStudio is moving from a document-chat/reporting application toward a
multi-discipline building-engineering agent. The roadmap preserves the product
phases while making GSD `.planning/` the primary planning system.
Completed graph, compliance, retrieval, and demo-backend work is recorded; the
remaining work is organized around frontend demo delivery, governance,
standards, data/cost services, MEP expansion, reporting, and 2D editing.

## Phases

- [x] **Phase 0: Governance And Planning Migration** - Agent instructions,
      task manifest migration, GSD planning migration, and GSD-compatible
      Jules automation bridge.
- [x] **Phase 1: Graph Foundation** - Canonical graph schema, fixtures,
      validation, persistence design, and graph database decision records.
- [ ] **Phase 2: Parser And Conversion Pipeline** - Optional parser engines,
      YOLO/IFC planning, and graph artifact persistence.
- [ ] **Phase 3: Compliance And Standards** - Deterministic standards,
      GOST-oriented ingestion, external-source policy, and evidence contracts.
- [ ] **Phase 4: Databases And RAG** - Authoritative graph storage path,
      real-estate data, property RAG fixtures, and hybrid retrieval.
- [ ] **Phase 5: Multidiscipline Engineering** - Electrical, plumbing,
      ventilation, HVAC, candidate fixes, and agent warning workflow.
- [ ] **Phase 6: 2D Editing And Review UI** - Graph/compliance inspection,
      graph-to-3D twin, roadmap view, and architecture/electrical editors.
- [ ] **Phase 7: Cost, ROI, And Reporting** - Cost calculators, ROI scenario
      service, and compliance evidence in report generation.
- [ ] **Phase 8: Demo Packaging And Disclosure** - Offline golden demo
      frontend, smoke tests, honesty docs, upstream logs, and runbooks.

## Phase Details

### Phase 0: Governance And Planning Migration

**Goal**: Make planning, autonomous task selection, and repository guardrails
explicit and GSD-native.

**Depends on**: Nothing.

**Requirements**: GOV-01, GOV-02, GOV-03, TASK-01

**Success Criteria** (what must be TRUE):

1. Future agents read `.planning/` only for active planning state.
2. The migrated task queue is available under `.planning/todos/`.
3. GSD project, requirements, roadmap, and state files exist.
4. Legacy planning files, task manifests, and validators are removed after GSD
   migration.
5. Retained Jules automation workflows read `.planning/` and do not depend on
   legacy task manifests.

**Plans**: 4 plans

Plans:

- [x] 00-01: Create repository-local agent guidance and planning docs.
- [x] 00-02: Migrate legacy task manifest into the GSD task queue.
- [x] 00-03: Migrate existing planning files into GSD `.planning/`.
- [x] 00-04: Add local agent task bridge CLI.

### Phase 1: Graph Foundation

**Goal**: Establish the canonical engineering graph and deterministic graph
validation contracts that every parser, checker, editor, and report can use.

**Depends on**: Phase 0

**Requirements**: GRAPH-01, GRAPH-02, GRAPH-03, GRAPH-04, GRAPH-05, GRAPH-06,
FLOW-01

**Success Criteria** (what must be TRUE):

1. Graph fixtures validate without live external services.
2. Graph artifacts have provenance and persistence design.
3. FlowDraft fusion behavior is represented behind existing backend services.
4. Future graph backend choices are documented with tradeoffs.

**Plans**: 7 plans

Plans:

- [x] 01-01: Define BlueprintStudio engineering graph schema v1.
- [x] 01-02: Import FlowDraft graph fixtures as test data.
- [x] 01-03: Add backend graph validation service.
- [x] 01-04: Design graph artifact persistence before database migration.
- [x] 01-05: Write graph database decision record.
- [x] 01-06: Port FlowDraft fusion into backend service.
- [ ] 01-07: Map graph concepts to BOT, IFC, Brick, and SHACL.

### Phase 2: Parser And Conversion Pipeline

**Goal**: Convert uploaded images, PDFs, and engineering exchange formats into
canonical graph artifacts through optional parser engines and fixture-backed
tests.

**Depends on**: Phase 1

**Requirements**: PARSE-01, PARSE-02, PARSE-03, PARSE-04

**Success Criteria** (what must be TRUE):

1. Parser contracts stay deterministic in tests.
2. YOLO, VLM, Roboflow, Claude, or similar engines remain optional.
3. Parser outputs can be validated and tied to uploaded documents.
4. IFC ingestion risks and fixtures are planned before implementation.

**Plans**: 4 plans

Plans:

- [x] 02-01: Define parser adapter contract for drawing conversion.
- [ ] 02-02: Plan YOLO-based drawing conversion integration.
- [ ] 02-03: Plan IFC ingestion spike.
- [ ] 02-04: Store parser outputs as graph artifacts tied to uploaded documents.

### Phase 3: Compliance And Standards

**Goal**: Build standards and compliance workflows around official-source
provenance, human-reviewed rules, deterministic checks, and evidence objects.

**Depends on**: Phase 1

**Requirements**: COMP-01, COMP-02, COMP-03, COMP-05, GOV-06

**Success Criteria** (what must be TRUE):

1. Compliance pass/fail behavior comes from deterministic rules.
2. Standards sources and extracted clauses carry provenance.
3. GOST-oriented ingestion is planned before scraping or live source access.
4. External-source access requires explicit policy and approval gates.

**Plans**: 5 plans

Plans:

- [x] 03-01: Port `dc_compliance_checker` rule model.
- [x] 03-02: Implement deterministic compliance validation runner.
- [x] 03-03: Create standards source catalog.
- [ ] 03-04: Plan GOST-oriented standards ingestion.
- [ ] 03-05: Define external source access policy.

### Phase 4: Databases And RAG

**Goal**: Combine authoritative graph retrieval with vector/text retrieval and
curated property/cost/standards datasets.

**Depends on**: Phase 1, Phase 3

**Requirements**: COMP-04, RAG-01, DATA-01, DATA-02

**Success Criteria** (what must be TRUE):

1. Vector/text retrieval is used for direct source lookup.
2. Graph retrieval is used for topology, connectivity, contradictions, and
   multi-hop reasoning.
3. Imported datasets include source, license, and provenance metadata.
4. Property price RAG fixtures are deterministic.

**Plans**: 4 plans

Plans:

- [x] 04-01: Index reviewed standards into vector RAG.
- [x] 04-02: Add hybrid graph and text retriever interface.
- [ ] 04-03: Create real-estate dataset catalog.
- [ ] 04-04: Add property price RAG fixture workflow.

### Phase 5: Multidiscipline Engineering

**Goal**: Expand graph-backed analysis across electrical, plumbing, HVAC,
ventilation, and agent candidate-fix workflows.

**Depends on**: Phase 1, Phase 3

**Requirements**: MEP-01, MEP-02, MEP-03, MEP-04, MEP-05, AGENT-01, AGENT-02

**Success Criteria** (what must be TRUE):

1. Electrical load and breaker checks remain deterministic.
2. PUE and BEC checks remain deterministic.
3. Plumbing and ventilation graph primitives are explicit.
4. Agent candidate fixes are traceable to evidence and require approval before
   write-back.

**Plans**: 5 plans

Plans:

- [x] 05-01: Port deterministic electrical load analysis.
- [x] 05-02: Port deterministic PUE and BEC checks.
- [x] 05-03: Define plumbing graph taxonomy.
- [ ] 05-04: Define ventilation graph taxonomy.
- [ ] 05-05: Add agent warning and candidate fix workflow.

### Phase 6: 2D Editing And Review UI

**Goal**: Give users deterministic inspection and editing surfaces for graph
objects, compliance findings, architectural geometry, and electrical layouts.

**Depends on**: Phase 1, Phase 5

**Requirements**: GRAPH-07, FLOW-08, FLOW-09, COMP-06, UI-01, UI-02, EDIT-01,
EDIT-02, EDIT-03, EDIT-04

**Success Criteria** (what must be TRUE):

1. Users can inspect graph objects and provenance in the frontend.
2. Users can review compliance evidence in the frontend.
3. Architecture and electrical editor designs protect graph integrity.
4. Editor MVPs update graph-backed state instead of decorative-only canvas
   state.

**Plans**: 8 plans

Plans:

- [ ] 06-01: Add frontend graph inspection view.
- [ ] 06-02: Add compliance results UI.
- [ ] 06-03: Add graph-to-3D twin frontend view.
- [ ] 06-04: Add capability roadmap view.
- [ ] 06-05: Design architecture 2D editor state model.
- [ ] 06-06: Build architecture 2D editor MVP.
- [ ] 06-07: Design electrical 2D editor state model.
- [ ] 06-08: Build electrical 2D editor MVP.

### Phase 7: Cost, ROI, And Reporting

**Goal**: Add deterministic cost and ROI calculations and extend reports with
engineering/compliance evidence.

**Depends on**: Phase 4, Phase 5

**Requirements**: FLOW-04, COST-01, COST-02, COMP-07, REPORT-01

**Success Criteria** (what must be TRUE):

1. Cost and ROI outputs expose inputs, assumptions, and provenance.
2. Deterministic calculators run before LLM explanation.
3. Reports include evidence without bypassing validation gates.
4. Existing report-session orchestration remains durable.

**Plans**: 4 plans

Plans:

- [x] 07-01: Add graph-derived property valuation demo service.
- [ ] 07-02: Implement approximate cost estimation service.
- [ ] 07-03: Add ROI and scenario calculation service.
- [ ] 07-04: Extend report pipeline with compliance evidence.

### Phase 8: Demo Packaging And Disclosure

**Goal**: Package the FlowDraft-inspired offline golden demo honestly and
repeatably inside BlueprintStudio.

**Depends on**: Phase 1, Phase 3, Phase 7

**Requirements**: GOV-04, GOV-05, FLOW-02, FLOW-03, FLOW-05, FLOW-06, FLOW-07

**Success Criteria** (what must be TRUE):

1. `Load demo` works without file uploads, API keys, model weights, or external
   network calls.
2. Rooms, valuation, and compliance tabs render deterministic fixture data.
3. Smoke tests prove the offline demo path.
4. Capability disclosure clearly separates working, partial, mocked, hardcoded,
   external, and roadmap features.
5. Docker/juror guidance exists only after the offline demo path is stable.

**Plans**: 7 plans

Plans:

- [x] 08-01: Refresh FlowDraft golden demo fixtures.
- [x] 08-02: Add FlowDraft-style demo and overlay API surfaces.
- [ ] 08-03: Add frontend golden demo workflow.
- [ ] 08-04: Add offline golden demo smoke test.
- [ ] 08-05: Add CrashPine upstream recheck log.
- [ ] 08-06: Add demo capability honesty disclosure.
- [ ] 08-07: Add deterministic demo Docker runbook.

## Backlog

Backlog and raw idea intake from the previous planning files are now represented
in:

- `todos/AGENT-TASKS.md`
- `seeds/SEED-001-team-direction.md`

## Progress

**Execution Order:** Future GSD execution should use the first safe pending task
from `todos/AGENT-TASKS.md` unless the user explicitly selects a phase.

| Phase | Milestone | Plans Complete | Status | Completed |
|-------|-----------|----------------|--------|-----------|
| 0. Governance And Planning Migration | v0 Planning | 4/4 | Complete | 2026-06-07 |
| 1. Graph Foundation | v1 Graph | 6/7 | In progress | - |
| 2. Parser And Conversion Pipeline | v1 Graph | 1/4 | In progress | - |
| 3. Compliance And Standards | v1 Compliance | 3/5 | In progress | - |
| 4. Databases And RAG | v1 Retrieval | 2/4 | In progress | - |
| 5. Multidiscipline Engineering | v1 Engineering | 3/5 | In progress | - |
| 6. 2D Editing And Review UI | v1 UI | 0/8 | Not started | - |
| 7. Cost, ROI, And Reporting | v1 Reporting | 1/4 | In progress | - |
| 8. Demo Packaging And Disclosure | v1 Demo | 2/7 | In progress | - |

---
*Roadmap migrated: 2026-06-07*
