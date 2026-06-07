import json
from pathlib import Path

from app.services.graph_validator import validate_graph


def test_valid_fixture_graph():
    """Valid fixture graph passes validation"""
    fixture_path = Path(__file__).parent.parent / "fixtures" / "graphs" / "architecture_only.json"
    data = json.loads(fixture_path.read_text())

    errors = validate_graph(data)
    assert not errors


def test_invalid_missing_node_edge_fails():
    """Invalid missing-node edge fails with a structured error"""
    data = {
        "edges": [{"edge_id": "e1", "source_id": "n1", "target_id": "n2", "discipline": "general"}]
    }
    errors = validate_graph(data)
    assert len(errors) == 2
    assert any(e.code == "missing_node" and e.path == "edges.0.source_id" for e in errors)
    assert any(e.code == "missing_node" and e.path == "edges.0.target_id" for e in errors)


def test_invalid_discipline_fails():
    """Invalid discipline or unsupported node type fails with a structured error"""
    data = {
        "nodes": [
            {
                "node_id": "n1",
                "discipline": "magic",  # invalid literal
            }
        ]
    }
    errors = validate_graph(data)
    assert len(errors) == 1
    assert errors[0].path == "nodes.0.discipline"
    assert errors[0].code == "invalid_value"
    assert errors[0].severity == "error"


def test_unsupported_node_type_fails():
    """Unsupported element fields fail with extra_forbidden."""
    data = {"nodes": [{"node_id": "n1", "unsupported_field": "test"}]}
    errors = validate_graph(data)
    assert len(errors) == 1
    assert errors[0].path == "nodes.0.unsupported_field"
    assert errors[0].code == "unsupported_field"
    assert errors[0].severity == "error"
