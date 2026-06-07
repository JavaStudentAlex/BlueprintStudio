"""Tests for the HybridRetriever combining FakeKB and GraphArtifactRegistry."""

from __future__ import annotations

import json
import sqlite3
from pathlib import Path

import pytest

from app.kb.fake import FakeKB
from app.schemas import EngineeringGraph
from app.services.graph_artifacts import GraphArtifactRegistry
from app.services.hybrid_retriever import HybridRetriever


@pytest.fixture
def registry():
    conn = sqlite3.connect(":memory:", check_same_thread=False)
    reg = GraphArtifactRegistry(conn)
    yield reg
    reg.close()


@pytest.fixture
def kb() -> FakeKB:
    return FakeKB()


@pytest.fixture
def fused_graph() -> EngineeringGraph:
    fixtures_dir = Path(__file__).parent.parent / "fixtures" / "graphs"
    fused_path = fixtures_dir / "fused_graph.json"
    data = json.loads(fused_path.read_text())
    return EngineeringGraph.model_validate(data)


@pytest.mark.asyncio
async def test_hybrid_retriever_combines_evidence(
    kb: FakeKB, registry: GraphArtifactRegistry, fused_graph: EngineeringGraph
) -> None:
    # 1. Setup FakeKB with text
    await kb.remember("The chiller clause states that chillers must have a PUE < 1.2.")
    await kb.remember("Irrelevant text.")

    # 2. Setup Registry with graph
    document_id = "doc-fused-123"
    registry.store_artifact(fused_graph, document_id=document_id)

    # 3. Retrieve
    retriever = HybridRetriever(kb, registry)
    result = await retriever.retrieve("chiller clause", document_id=document_id)

    # 4. Verify Text Evidence
    assert len(result.text_evidence) == 1
    assert "chiller clause" in result.text_evidence[0]["content"]

    # 5. Verify Graph Evidence
    assert len(result.graph_evidence) == 1
    graph_evidence = result.graph_evidence[0]

    # Check that chiller nodes were found
    node_names = [n.get("properties", {}).get("name") for n in graph_evidence.nodes]
    assert "CH-1" in node_names
    assert "CH-2" in node_names

    # Check that enclosing space was brought into the neighborhood
    space_names = [s.get("properties", {}).get("name") for s in graph_evidence.spaces]
    assert "Data Hall A" in space_names


@pytest.mark.asyncio
async def test_hybrid_retriever_no_evidence(
    kb: FakeKB, registry: GraphArtifactRegistry, fused_graph: EngineeringGraph
) -> None:
    document_id = "doc-fused-456"
    registry.store_artifact(fused_graph, document_id=document_id)

    retriever = HybridRetriever(kb, registry)
    result = await retriever.retrieve("completely unknown thing", document_id=document_id)

    assert len(result.text_evidence) == 0
    assert len(result.graph_evidence) == 0
