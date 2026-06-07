import sqlite3

import pytest

from app.schemas import EngineeringGraph, GraphMeta, GraphNode, GraphProvenance
from app.services.graph_artifacts import GraphArtifactRegistry


@pytest.fixture
def registry():
    conn = sqlite3.connect(":memory:", check_same_thread=False)
    reg = GraphArtifactRegistry(conn)
    yield reg
    reg.close()


def test_store_and_retrieve_by_document_id(registry: GraphArtifactRegistry):
    document_id = "doc_123"
    graph = EngineeringGraph(
        meta=GraphMeta(title="Test Graph"),
        nodes=[
            GraphNode(
                node_id="node_1",
                category="equipment",
                provenance=GraphProvenance(source_file="doc.pdf", confidence=0.9),
            )
        ],
    )

    record = registry.store_artifact(graph, document_id=document_id)
    assert record.artifact_id is not None
    assert record.document_id == document_id
    assert record.project_id is None
    assert record.schema_version == "1.0"

    retrieved = registry.get_by_document_id(document_id)
    assert len(retrieved) == 1
    assert retrieved[0].artifact_id == record.artifact_id
    assert len(retrieved[0].graph_data.nodes) == 1

    node = retrieved[0].graph_data.nodes[0]
    assert node.node_id == "node_1"
    assert node.provenance is not None
    assert node.provenance.source_file == "doc.pdf"


def test_store_and_retrieve_by_project_id(registry: GraphArtifactRegistry):
    project_id = "proj_456"
    graph = EngineeringGraph(meta=GraphMeta(title="Project Graph"))

    record = registry.store_artifact(graph, project_id=project_id, schema_version="1.1")
    assert record.project_id == project_id
    assert record.document_id is None
    assert record.schema_version == "1.1"

    retrieved = registry.get_by_project_id(project_id)
    assert len(retrieved) == 1
    assert retrieved[0].artifact_id == record.artifact_id
    assert retrieved[0].graph_data.meta.title == "Project Graph"


def test_store_requires_document_or_project(registry: GraphArtifactRegistry):
    graph = EngineeringGraph()
    with pytest.raises(ValueError, match="must provide either document_id or project_id"):
        registry.store_artifact(graph)


def test_retrieve_ordering_is_newest_first(registry: GraphArtifactRegistry):
    document_id = "doc_order"

    reg1 = registry.store_artifact(
        EngineeringGraph(meta=GraphMeta(title="First")), document_id=document_id
    )
    reg2 = registry.store_artifact(
        EngineeringGraph(meta=GraphMeta(title="Second")), document_id=document_id
    )

    retrieved = registry.get_by_document_id(document_id)
    assert len(retrieved) == 2
    assert retrieved[0].artifact_id == reg2.artifact_id
    assert retrieved[1].artifact_id == reg1.artifact_id
