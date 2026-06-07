import json
from pathlib import Path
from app.schemas import EngineeringGraph

FIXTURES_DIR = Path(__file__).parent / "fixtures" / "graphs"


def test_architecture_fixture_is_valid():
    with open(FIXTURES_DIR / "architecture_only.json") as f:
        data = json.load(f)
    graph = EngineeringGraph(**data)
    assert graph.meta.diagram_type == "floorplan"
    assert len(graph.spaces) > 0


def test_mep_fixture_is_valid():
    with open(FIXTURES_DIR / "mep_only.json") as f:
        data = json.load(f)
    graph = EngineeringGraph(**data)
    assert graph.meta.diagram_type == "sld"
    assert len(graph.fixtures) > 0


def test_fused_fixture_is_valid():
    with open(FIXTURES_DIR / "fused_graph.json") as f:
        data = json.load(f)
    graph = EngineeringGraph(**data)
    assert graph.meta.diagram_type == "fused"
    assert len(graph.spaces) > 0
    assert len(graph.fixtures) > 0
