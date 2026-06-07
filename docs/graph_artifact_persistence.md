# Graph Artifact Persistence Design

## Context

BlueprintStudio involves extracting engineering facts (spaces, equipment, topology) from uploaded construction documents and reasoning about them. We need a way to persist the parsed "engineering graph" for these documents and projects.

## Why MemoryPalace is Not the Engineering Source of Truth

MemoryPalace is designed primarily for agent memory and document recall via vector embeddings (pgvector), text RAG, and general conversational history. However, it is not suitable as the authoritative engineering source of truth for the following reasons:

1. **Topology and Exact Schemas:** Engineering graphs require strict structural contracts, exact coordinate and topology mapping, and relationships that can be deterministically validated (e.g., node A must connect to node B). MemoryPalace is optimized for unstructured or semi-structured semantic retrieval, not strict topological integrity.
2. **Deterministic Rules:** We need to run deterministic rule engines against the graph (e.g., compliance checks, area checks). Extracting an exact sub-graph from vector embeddings is unreliable.
3. **Graph Retrieval Needs:** Engineering operations require multi-hop relationship traversal, which is native to graph structures but challenging and inefficient in vector or relational text-based storage.

## Initial Persistence Strategy: SQLite JSON Storage

While the ultimate goal is to transition to a dedicated graph database (such as Neo4j, TuGraph, or NebulaGraph) or an RDF/semantic graph backend, we must avoid premature coupling. An immediate leap to a specific graph database adds significant deployment complexity, infrastructure dependency, and vendor lock-in before the data model itself is fully stabilized.

To balance immediate product needs with architectural safety, the first persistence layer for parsed graph artifacts will be a **SQLite-backed registry storing JSON artifacts**.

### Advantages of the SQLite Approach

- **Zero-Dependency Setup:** It works locally and in tests without requiring external services or docker containers for graph databases.
- **Flexibility:** JSON columns (or text fields holding JSON) allow us to store the full `EngineeringGraph` payloads, preserving exact schema versions and source provenance.
- **Queryability:** We can easily query and retrieve stored graph artifacts by `document_id` or `project_id`.
- **Easy Migration:** When the graph schema stabilizes and the need for complex multi-hop queries outweighs the simplicity of SQLite, we can migrate the JSON payloads to a dedicated graph database with minimal friction.

## Schema Versioning and Provenance

Every stored graph artifact will include:
- `schema_version`: To gracefully handle future changes in the `EngineeringGraph` schema.
- Source provenance: Extracted graphs will preserve the source file, parser engine, and confidence values mapping back to the exact parsed locations within the uploaded documents.

This design ensures we have a safe, testable, and robust persistence layer that fulfills current engineering needs without complicating the immediate development and deployment pipelines.
