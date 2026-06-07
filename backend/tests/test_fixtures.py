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


def test_flowdraft_fixtures_are_valid():
    flowdraft_dir = Path(__file__).parent / "fixtures" / "flowdraft"

    # Floorplan fixture
    with open(flowdraft_dir / "demo_floorplan.json") as f:
        data = json.load(f)
    graph = EngineeringGraph(**data)
    assert graph.meta.diagram_type == "FLOORPLAN"
    assert len(graph.spaces) > 0

    # Datacentre fixture
    with open(flowdraft_dir / "demo_datacentre.json") as f:
        data = json.load(f)
    graph = EngineeringGraph(**data)
    assert graph.meta.diagram_type == "FUSED"
    assert len(graph.spaces) > 0
    assert len(graph.nodes) > 0

    # Mock graph fixture
    with open(flowdraft_dir / "mock_graph.json") as f:
        data = json.load(f)
    graph = EngineeringGraph(**data)
    assert graph.meta.diagram_type == "PID"
    assert len(graph.nodes) > 0


def test_flowdraft_compliance_report_is_valid():
    flowdraft_dir = Path(__file__).parent / "fixtures" / "flowdraft"
    with open(flowdraft_dir / "demo_compliance_report.json") as f:
        data = json.load(f)
    assert "checks_run" in data
    assert "passed" in data
    assert "violations" in data
