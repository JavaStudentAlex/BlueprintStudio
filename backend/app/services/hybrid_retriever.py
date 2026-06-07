"""Hybrid retrieval combining text from KnowledgeBase and structure from GraphArtifactRegistry."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from app.kb.base import KnowledgeBase, MemoryRecord
from app.schemas import EngineeringGraph
from app.services.graph_artifacts import GraphArtifactRegistry


@dataclass(frozen=True, slots=True)
class GraphEvidence:
    """Evidence extracted from an engineering graph based on a query."""

    source_artifact_id: str
    nodes: list[dict[str, Any]]
    spaces: list[dict[str, Any]]
    fixtures: list[dict[str, Any]]
    edges: list[dict[str, Any]]


@dataclass(frozen=True, slots=True)
class HybridRetrievalResult:
    """Combined text and graph evidence."""

    text_evidence: list[MemoryRecord]
    graph_evidence: list[GraphEvidence]


class HybridRetriever:
    """Retrieves combined text and graph evidence for a query."""

    def __init__(self, kb: KnowledgeBase, registry: GraphArtifactRegistry) -> None:
        self._kb = kb
        self._registry = registry

    async def retrieve(
        self,
        query: str,
        *,
        document_id: str | None = None,
        project_id: str | None = None,
        k_text: int = 5,
    ) -> HybridRetrievalResult:
        """Fetch matching text memories and relevant graph topology."""
        # 1. Fetch text evidence
        text_records = await self._kb.recall(query, k=k_text)

        # 2. Fetch graph evidence
        graph_evidence: list[GraphEvidence] = []
        from app.services.graph_artifacts import GraphArtifactRecord
        artifacts: list[GraphArtifactRecord] = []
        if document_id:
            artifacts.extend(self._registry.get_by_document_id(document_id))
        elif project_id:
            artifacts.extend(self._registry.get_by_project_id(project_id))

        query_lower = query.lower()

        for artifact in artifacts:
            graph = artifact.graph_data
            evidence = self._extract_graph_neighborhood(graph, query_lower, artifact.artifact_id)
            if self._has_evidence(evidence):
                graph_evidence.append(evidence)

        return HybridRetrievalResult(
            text_evidence=text_records,
            graph_evidence=graph_evidence,
        )

    def _extract_graph_neighborhood(
        self, graph: EngineeringGraph, query_lower: str, artifact_id: str
    ) -> GraphEvidence:
        matched_nodes = []
        matched_spaces = []
        matched_fixtures = []

        # Find matching nodes
        for node in graph.nodes:
            if self._matches(node, query_lower):
                matched_nodes.append(node)

        # Find matching spaces
        for space in graph.spaces:
            if self._matches(space, query_lower):
                matched_spaces.append(space)

        # Find matching fixtures
        for fixture in graph.fixtures:
            if self._matches(fixture, query_lower):
                matched_fixtures.append(fixture)

        # Expand neighborhood: include spaces containing matched nodes/fixtures
        space_ids_to_include = {s.space_id for s in matched_spaces}
        for node in matched_nodes:
            if node.space_id:
                space_ids_to_include.add(node.space_id)
        for fixture in matched_fixtures:
            if fixture.space_id:
                space_ids_to_include.add(fixture.space_id)

        # Find additional spaces
        for space in graph.spaces:
            if space.space_id in space_ids_to_include and space not in matched_spaces:
                matched_spaces.append(space)

        # Expand neighborhood: include nodes/fixtures in matched spaces
        for node in graph.nodes:
            if node.space_id in space_ids_to_include and node not in matched_nodes:
                matched_nodes.append(node)
        for fixture in graph.fixtures:
            if fixture.space_id in space_ids_to_include and fixture not in matched_fixtures:
                matched_fixtures.append(fixture)

        # Expand neighborhood: include connected edges
        node_ids = {n.node_id for n in matched_nodes}
        matched_edges = []
        for edge in graph.edges:
            if edge.source_id in node_ids or edge.target_id in node_ids:
                matched_edges.append(edge)

        # Also include nodes connected by matched edges
        connected_node_ids = set()
        for edge in matched_edges:
            if edge.source_id not in node_ids:
                connected_node_ids.add(edge.source_id)
            if edge.target_id not in node_ids:
                connected_node_ids.add(edge.target_id)

        for node in graph.nodes:
            if node.node_id in connected_node_ids and node not in matched_nodes:
                matched_nodes.append(node)

        return GraphEvidence(
            source_artifact_id=artifact_id,
            nodes=[n.model_dump(exclude_none=True) for n in matched_nodes],
            spaces=[s.model_dump(exclude_none=True) for s in matched_spaces],
            fixtures=[f.model_dump(exclude_none=True) for f in matched_fixtures],
            edges=[e.model_dump(exclude_none=True) for e in matched_edges],
        )

    def _matches(self, obj: Any, query_lower: str) -> bool:
        # Split query into words to match independently
        query_words = [w.strip() for w in query_lower.split() if w.strip()]
        if not query_words:
            return False

        for word in query_words:
            matched = False
            if hasattr(obj, "properties") and obj.properties:
                for k, v in obj.properties.items():
                    if word in str(k).lower() or word in str(v).lower():
                        matched = True
                        break
            if not matched and hasattr(obj, "category") and obj.category and word in obj.category.lower():
                matched = True

            if matched:
                return True
        return False

    def _has_evidence(self, evidence: GraphEvidence) -> bool:
        return bool(evidence.nodes or evidence.spaces or evidence.fixtures or evidence.edges)
