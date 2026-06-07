# BlueprintStudio Backlog

## Instructions For Agents

Use `agent_tasks.json` as the machine-readable source of truth. This backlog is
for human-readable planning and product direction. When taking work from this
file, create or update an explicit task in `agent_tasks.json` first.

## Strategic Direction

BlueprintStudio should evolve into a multi-discipline building-engineering
agent with:

- document ingestion and report generation
- graph-backed architecture and MEP understanding
- deterministic compliance checks
- standards and regulation RAG
- real-estate and cost-data retrieval
- approximate cost and ROI estimates
- 2D editing for architecture and electrical systems
- future support for plumbing, HVAC, ventilation, data-centres, and other
  engineering disciplines

## Architecture And Database

- [ ] Define the canonical BlueprintStudio engineering graph schema.
- [ ] Decide and document the first authoritative graph persistence strategy.
- [ ] Keep MemoryPalace as agent memory/document recall, not the engineering
      source of truth.
- [ ] Add graph provenance and temporal validity fields.
- [ ] Add hybrid retrieval: vector/text RAG plus graph retrieval.
- [ ] Add GraphRAG only after graph contracts and deterministic validation are
      stable.
- [ ] Evaluate Neo4j, TuGraph, NebulaGraph, and RDF/SHACL options.

## FlowDraft Fusion

- [ ] Map FlowDraft schema to BlueprintStudio graph schema.
- [ ] Import FlowDraft demo graphs as fixtures.
- [ ] Port graph validation into the backend.
- [ ] Port fusion service: floor plan plus MEP graph to fused graph.
- [ ] Port deterministic PUE and BEC checks.
- [ ] Port electrical load and breaker headroom checks.
- [ ] Adapt FlowDraft ROI/property estimation to a proper dataset service.
- [ ] Add parser adapter contracts for floor plan, PID, SLD, and data-centre
      diagrams.
- [ ] Keep parser engines optional and test with fixtures.

## FlowDraft Golden Demo Refresh

- [ ] Track the latest reviewed FlowDraft commit before implementation work.
- [ ] Import only sanitized frozen demo JSON fixtures: floor-plan graph,
      compliance report, and compliance test graph.
- [ ] Add backend demo endpoints for frozen floor-plan and compliance fixtures.
- [ ] Add an overlay rendering service that works from graph JSON and uploaded
      images without writing generated assets to git.
- [ ] Add graph-derived property valuation with dataset provenance and clear
      assumptions.
- [ ] Add a frontend `Load demo` flow with Overlay, Rooms, Valuation, and
      Compliance views in the existing Next.js shell.
- [ ] Add an end-to-end demo smoke test that proves the offline demo path works
      without external API keys.

## Compliance And Standards

- [ ] Port `dc_compliance_checker` rule and violation models.
- [ ] Convert compliance rules into typed backend schemas.
- [ ] Add deterministic validation for numeric, existence, and topology rules.
- [ ] Add standards source catalog with provenance.
- [ ] Add GOST-oriented standards ingestion plan.
- [ ] Add AI-assisted rule extraction with human review.
- [ ] Add violation evidence output: rule, object, actual, expected, source,
      confidence, and candidate fixes.

## Real-Estate And Cost Data

- [ ] Define a dataset catalog for property, prices, rents, construction costs,
      equipment costs, and standards.
- [ ] Add source provenance and license metadata for every imported dataset.
- [ ] Add vector indexes for curated source summaries.
- [ ] Add deterministic cost calculators before LLM explanation.
- [ ] Add agent workflows for approximate pricing and ROI.

## Multidiscipline Engineering

- [ ] Define discipline taxonomy for architecture, electrical, plumbing, HVAC,
      ventilation, fire safety, and data-centres.
- [ ] Add electrical graph primitives: panels, circuits, loads, cable paths,
      protective devices, and schedules.
- [ ] Add plumbing graph primitives: pipes, fixtures, valves, risers, pumps,
      drains, and meters.
- [ ] Add ventilation graph primitives: fans, AHUs, ducts, dampers, diffusers,
      zones, and airflow edges.
- [ ] Add checks for connectivity, capacity, missing equipment, and impossible
      topology.

## 2D Editing

- [ ] Define 2D editor architecture and state model.
- [ ] Build architecture editor MVP: walls, rooms, openings, labels, dimensions.
- [ ] Build electrical editor MVP: panels, circuits, fixtures, outlets, cable
      paths.
- [ ] Add layer toggles for architecture, electrical, plumbing, HVAC, and
      compliance.
- [ ] Make edits update the canonical engineering graph.
- [ ] Add validation overlays and issue annotations.

## Agent And Reports

- [ ] Add graph/text hybrid retrieval to the agent.
- [ ] Add warning-to-evidence-to-fix workflow.
- [ ] Extend report generation for compliance, engineering, cost, and ROI.
- [ ] Add human approval before graph write-back for physical or compliance
      changes.
- [ ] Add task bridge for autonomous Jules/Codex work.

## Completed Planning Work

- [x] Create repository-local agent guidance.
- [x] Inspect Magda-agent task direction pattern.
- [x] Import and adapt visual-odometry agent instruction surface.
- [x] Create BlueprintStudio planning docs and task manifest.
