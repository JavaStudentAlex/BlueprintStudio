# Graph Database Decision Record

## Context and Problem Statement

BlueprintStudio requires an authoritative engineering source of truth to store and reason about building engineering properties, topologies, relationships, and multi-discipline structures.

The immediate requirement is met by storing canonical JSON artifacts backed by SQLite (`graph_artifact_persistence.md`), but a true long-term graph model needs to be identified. The long-term architecture requires a robust strategy for complex multi-hop engineering relationships (such as circuit tracing, pipe connectivity, or air flow constraints) and compliance validations against regulations.

This document serves to evaluate graph/database backend options and determine the path forward for the canonical engineering graph persistence and reasoning, particularly outlining GraphRAG usage boundaries.

## Evaluation Criteria

Any long-term graph database candidate must be evaluated against the following criteria:

- **Expressiveness:** Can it model multi-discipline domains (architecture, electrical, HVAC) and handle complex graph properties?
- **Query Performance:** Can it efficiently execute deep graph traversals (multi-hop) for topology checks and load calculations?
- **Integration:** How easily does it integrate with the LangGraph/FastAPI Python backend and LLM workflows (GraphRAG)?
- **Validation Capabilities:** Does it natively support strict schema/ontology enforcement or rule-based semantic validation?
- **Deployment Complexity:** Does it require heavy standalone clusters or vendor lock-in? Is local execution viable?

## Evaluated Options

We analyzed a series of database and graph solutions for BlueprintStudio:

1. **Neo4j:**
   - *Pros:* Industry-standard property graph, strongest Python/LangChain integration, optimal for GraphRAG and multi-hop queries, robust pathfinding.
   - *Cons:* Heavy footprint, complex local deployment if full enterprise features are needed.
2. **TuGraph / NebulaGraph / HugeGraph:**
   - *Pros:* High performance, high scalability for massive datasets.
   - *Cons:* Lower adoption in typical LangGraph/RAG pipelines, often overkill for single-building sizes, fewer mature Python integrations compared to Neo4j.
3. **Memgraph:**
   - *Pros:* In-memory, high-performance, Cypher-compatible, lighter footprint than Neo4j.
   - *Cons:* Requires enough RAM to hold the graph, potentially tricky for very large building portfolios if scaled prematurely.
4. **RDF / OWL / SHACL:**
   - *Pros:* Unmatched for semantic validation and strict engineering/compliance ontologies (e.g., standard compliance). SHACL allows deterministic semantic rule evaluation.
   - *Cons:* Difficult to query (SPARQL can be cumbersome for developers), poorer GraphRAG integrations out-of-the-box compared to property graphs.
5. **PostgreSQL (JSONB or pgvector):**
   - *Pros:* Familiar, already used with MemoryPalace, solid for relational and document data, vector search built-in.
   - *Cons:* Extremely inefficient for deep multi-hop topology and graph traversals. Not a true graph database.
6. **MemoryPalace (Current baseline context):**
   - *Pros:* Excellent for agent memory, document recall, and text RAG.
   - *Cons:* Unstructured or semi-structured, cannot enforce strict topological integrity or run deterministic graph validations. It is not the engineering source of truth.

## Decision

### Short-Term Storage Strategy
We will continue using **SQLite + JSON** as the short-term storage strategy for graph artifacts.
- *Why:* Zero dependency overhead, highly flexible, easily allows graph artifacts to be tied to document/project IDs. As established in `graph_artifact_persistence.md`, this meets immediate MVP needs without premature infrastructure commitment.

### Long-Term Storage Strategy
The long-term storage architecture will be a **hybrid approach**:
1. **Neo4j** will be adopted as the primary property graph database for the fast GraphRAG, topology reasoning, multi-hop pathfinding, and multi-discipline engineering analytics path.
2. **RDF/OWL and SHACL** paradigms will be utilized or bridged for strict, deterministic standards and semantic validation (e.g., GOST compliance rules), potentially overlaying the primary graph.

### Usage of GraphRAG

GraphRAG is a powerful tool but must be strictly bounded in BlueprintStudio to avoid hallucinations and maintain deterministic engineering facts.

**When to use GraphRAG:**
- Complex topology exploration and multi-hop reasoning (e.g., "What spaces are impacted if this electrical panel fails?").
- Finding contradictions in connectivity.
- Exploring system hierarchies and missing functional links.
- Impact analysis across multi-discipline domains (e.g., HVAC units relative to architectural zones).

**When NOT to use GraphRAG:**
- Deterministic numeric compliance checks (e.g., calculating exact area, width, or specific PUE).
- Simple factual or direct clause lookup (e.g., "What is the text of GOST clause 4.2?"). Use standard vector/text RAG for this.
- Physical or compliance-impacting graph write-backs without an explicit human-in-the-loop approval gate.

## Open Questions

- *Migration Path:* When exactly should the shift from SQLite JSON payloads to the fully deployed Neo4j instance happen? (Likely post-Phase 4, when the canonical graph schema is fully hardened).
- *Ontology Bridging:* How will we practically bridge the Neo4j property graph format into a semantic/RDF validation tool for SHACL rule compliance?
- *Viewer Performance:* Will pulling massive graph topologies directly from Neo4j into the frontend 3D/2D viewer require an intermediate edge-cache layer?
