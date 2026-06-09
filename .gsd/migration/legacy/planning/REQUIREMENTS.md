# Requirements: BlueprintStudio

**Defined:** 2026-06-07  
**Core Value:** BlueprintStudio must convert construction and engineering
document context into traceable, testable engineering evidence before an agent
explains, reports, or proposes changes.

## v1 Requirements

### Governance

- [x] **GOV-01**: Repository-local agent guidance defines task source priority,
      domain contracts, verification gates, and guardrails.
- [x] **GOV-02**: The legacy autonomous task manifest was migrated into the GSD
      task queue.
- [x] **GOV-03**: GSD `.planning/` is the primary planning entry point for
      future agent work.
- [ ] **GOV-04**: CrashPine and FlowDraft upstream references are recorded with
      reviewed commit SHAs before implementation batches.
- [ ] **GOV-05**: Capability honesty documentation separates live, beta, mocked,
      hardcoded, externally dependent, and roadmap behavior.
- [ ] **GOV-06**: External source access policy defines when standards,
      government sites, paid APIs, and scraping require human approval.

### Engineering Graph

- [x] **GRAPH-01**: BlueprintStudio has a canonical engineering graph schema v1.
- [x] **GRAPH-02**: FlowDraft graph fixtures are available as deterministic test
      data.
- [x] **GRAPH-03**: Backend graph validation checks schema and graph integrity.
- [x] **GRAPH-04**: Graph artifact persistence strategy is designed before
      database migration.
- [x] **GRAPH-05**: Graph database decision record evaluates Neo4j, TuGraph,
      NebulaGraph, RDF/OWL, SHACL, PostgreSQL JSONB, and SQLite fixture paths.
- [ ] **GRAPH-06**: Graph concepts are mapped to BOT, IFC, Brick, and SHACL
      where useful for standards and interoperability.
- [ ] **GRAPH-07**: Frontend graph inspection lets users inspect graph objects,
      provenance, warnings, and relationships.

### FlowDraft And Demo

- [x] **FLOW-01**: FlowDraft fusion behavior is ported behind backend services
      rather than copied as a separate app.
- [x] **FLOW-02**: Golden demo fixtures are sanitized and deterministic.
- [x] **FLOW-03**: Backend demo and overlay surfaces expose fixture-backed demo
      behavior without API keys.
- [x] **FLOW-04**: Graph-derived property valuation demo service exposes clear
      assumptions and provenance.
- [ ] **FLOW-05**: The existing Next.js shell has an offline `Load demo` flow
      with Overlay, Rooms, Valuation, and Compliance views.
- [ ] **FLOW-06**: Offline golden demo e2e smoke coverage proves the demo path
      works from committed fixtures only.
- [ ] **FLOW-07**: Demo Docker/juror runbook support exists after the offline
      demo path is stable.
- [ ] **FLOW-08**: Graph-to-3D twin view consumes the canonical graph contract.
- [ ] **FLOW-09**: Capability roadmap view labels live, beta, mocked, and
      roadmap items clearly.

### Parsing And Conversion

- [x] **PARSE-01**: Parser adapter contracts define drawing conversion inputs,
      outputs, validation, and fixture behavior.
- [ ] **PARSE-02**: YOLO-based drawing conversion integration is planned with
      optional engines and no default-test external calls.
- [ ] **PARSE-03**: IFC ingestion spike is planned with scope, risks, fixtures,
      and expected graph output.
- [ ] **PARSE-04**: Parser outputs are stored as graph artifacts tied to
      uploaded documents with provenance.

### Compliance And Standards

- [x] **COMP-01**: `dc_compliance_checker` rule and violation model concepts are
      ported into backend contracts.
- [x] **COMP-02**: Deterministic compliance validation runner handles numeric,
      existence, and topology rules.
- [x] **COMP-03**: Standards source catalog captures provenance for reviewed
      standards.
- [x] **COMP-04**: Reviewed standards can be indexed into vector RAG.
- [ ] **COMP-05**: GOST-oriented standards ingestion plan covers source catalog,
      clause extraction, human-reviewed normalization, and deterministic rules.
- [ ] **COMP-06**: Compliance results UI renders rule, object, actual,
      expected, source, confidence, and candidate fixes.
- [ ] **COMP-07**: Report pipeline includes compliance evidence without
      weakening human-in-the-loop gates.

### Retrieval, Data, Cost, And ROI

- [x] **RAG-01**: Hybrid graph and text retriever interface separates graph
      topology questions from direct text/vector lookups.
- [ ] **DATA-01**: Real-estate dataset catalog defines property, price, rent,
      construction-cost, equipment-cost, and standards sources.
- [ ] **DATA-02**: Property price RAG fixtures use curated data and explicit
      provenance.
- [ ] **COST-01**: Approximate cost estimation service uses deterministic
      calculators before LLM explanation.
- [ ] **COST-02**: ROI and scenario calculation service exposes assumptions,
      inputs, and provenance.

### Multidiscipline Engineering

- [x] **MEP-01**: Electrical load analysis computes deterministic loads,
      current, and breaker headroom.
- [x] **MEP-02**: PUE and BEC checks are deterministic services.
- [x] **MEP-03**: Plumbing graph taxonomy defines fixtures, pipes, valves,
      meters, drains, pumps, risers, and topology concepts.
- [ ] **MEP-04**: Ventilation graph taxonomy defines fans, AHUs, ducts,
      dampers, diffusers, zones, and airflow edges.
- [ ] **MEP-05**: Agent candidate fixes are based on graph evidence and ranked
      feasibility.

### UI And 2D Editing

- [ ] **UI-01**: Frontend graph inspection view uses canonical graph data.
- [ ] **UI-02**: Compliance report UI renders deterministic evidence clearly.
- [ ] **EDIT-01**: Architecture 2D editor design defines state model, geometry,
      layers, validation, and graph write-back.
- [ ] **EDIT-02**: Architecture 2D editor MVP supports walls, rooms, openings,
      labels, dimensions, and areas.
- [ ] **EDIT-03**: Electrical 2D editor design defines panels, circuits,
      fixtures, outlets, switches, cable paths, and schedules.
- [ ] **EDIT-04**: Electrical 2D editor MVP supports panels, circuits, fixtures,
      outlets, and cable paths.

### Agent And Reports

- [ ] **AGENT-01**: Agent warning workflow emits warning, evidence, violated
      rule or graph condition, confidence, provenance, and candidate fixes.
- [ ] **AGENT-02**: Graph write-back for physical or compliance-impacting
      changes requires human approval.
- [ ] **REPORT-01**: Reports can include compliance, engineering, cost, and ROI
      evidence without bypassing validation gates.
- [x] **TASK-01**: A local task bridge can validate, summarize, select, and
      render tasks from the migrated task queue.

## v2 Requirements

- **AI-01**: Live AI-assisted standards rule extraction can be added after the
  human-review and deterministic-rule contracts are stable.
- **PARSE-05**: Production YOLO, VLM, Roboflow, Claude, or other external parser
  engines can be enabled behind explicit configuration and non-default tests.
- **GRAPH-08**: Dedicated property graph, RDF/OWL, or SHACL backend migration
  can proceed after the graph artifact persistence design is validated.
- **EDIT-05**: Plumbing, HVAC, ventilation, fire-safety, and compliance editor
  layers can be added after architecture and electrical MVPs are stable.
- **DEMO-01**: Published Docker images or demo assets require explicit human
  approval and release process.

## Out of Scope

| Feature | Reason |
|---------|--------|
| LLM as compliance source of truth | Deterministic rule execution and source evidence must decide pass/fail. |
| Live external calls from default tests | Tests must remain deterministic and local. |
| Committing source drawings, uploads, generated reports, model weights, or local runtime state | These are sensitive, large, generated, or environment-specific. |
| Merging FlowDraft or CrashPine as a tree replacement | BlueprintStudio keeps its existing backend, frontend, tests, and repo structure. |
| Silent graph or report mutation by the agent | Engineering changes require visible evidence and user approval. |
| Workflow, secret, deployment, or auto-merge changes in ordinary tasks | These require explicit human approval. |

## Traceability

| Requirement | Phase | Status |
|-------------|-------|--------|
| GOV-01 | Phase 0 | Complete |
| GOV-02 | Phase 0 | Complete |
| GOV-03 | Phase 0 | Complete |
| GOV-04 | Phase 8 | Pending |
| GOV-05 | Phase 8 | Pending |
| GOV-06 | Phase 3 | Pending |
| GRAPH-01 | Phase 1 | Complete |
| GRAPH-02 | Phase 1 | Complete |
| GRAPH-03 | Phase 1 | Complete |
| GRAPH-04 | Phase 1 | Complete |
| GRAPH-05 | Phase 1 | Complete |
| GRAPH-06 | Phase 1 | Pending |
| GRAPH-07 | Phase 6 | Pending |
| FLOW-01 | Phase 1 | Complete |
| FLOW-02 | Phase 8 | Complete |
| FLOW-03 | Phase 8 | Complete |
| FLOW-04 | Phase 7 | Complete |
| FLOW-05 | Phase 8 | Pending |
| FLOW-06 | Phase 8 | Pending |
| FLOW-07 | Phase 8 | Pending |
| FLOW-08 | Phase 6 | Pending |
| FLOW-09 | Phase 6 | Pending |
| PARSE-01 | Phase 2 | Complete |
| PARSE-02 | Phase 2 | Pending |
| PARSE-03 | Phase 2 | Pending |
| PARSE-04 | Phase 2 | Pending |
| COMP-01 | Phase 3 | Complete |
| COMP-02 | Phase 3 | Complete |
| COMP-03 | Phase 3 | Complete |
| COMP-04 | Phase 4 | Complete |
| COMP-05 | Phase 3 | Pending |
| COMP-06 | Phase 6 | Pending |
| COMP-07 | Phase 7 | Pending |
| RAG-01 | Phase 4 | Complete |
| DATA-01 | Phase 4 | Pending |
| DATA-02 | Phase 4 | Pending |
| COST-01 | Phase 7 | Pending |
| COST-02 | Phase 7 | Pending |
| MEP-01 | Phase 5 | Complete |
| MEP-02 | Phase 5 | Complete |
| MEP-03 | Phase 5 | Complete |
| MEP-04 | Phase 5 | Pending |
| MEP-05 | Phase 5 | Pending |
| UI-01 | Phase 6 | Pending |
| UI-02 | Phase 6 | Pending |
| EDIT-01 | Phase 6 | Pending |
| EDIT-02 | Phase 6 | Pending |
| EDIT-03 | Phase 6 | Pending |
| EDIT-04 | Phase 6 | Pending |
| AGENT-01 | Phase 5 | Pending |
| AGENT-02 | Phase 5 | Pending |
| REPORT-01 | Phase 7 | Pending |
| TASK-01 | Phase 0 | Complete |

**Coverage:**

- v1 requirements: 54 total
- Mapped to phases: 54
- Unmapped: 0

---
*Requirements migrated: 2026-06-07*
*Last updated: 2026-06-07 after GSD planning migration*
