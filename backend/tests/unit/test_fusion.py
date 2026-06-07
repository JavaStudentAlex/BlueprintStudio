import json

from app.schemas import EngineeringGraph
from app.services.fusion import fuse_graphs, is_point_in_polygon


def test_is_point_in_polygon():
    polygon = [[0, 0], [10, 0], [10, 10], [0, 10]]
    assert is_point_in_polygon([5, 5], polygon) is True
    assert is_point_in_polygon([15, 5], polygon) is False
    assert is_point_in_polygon([5, 15], polygon) is False
    assert is_point_in_polygon([-5, 5], polygon) is False
    assert is_point_in_polygon([5, -5], polygon) is False


def test_fuse_graphs_fixture():
    # Load architectural graph fixture
    with open("tests/fixtures/graphs/architecture_only.json") as f:
        arch_data = json.load(f)
    arch = EngineeringGraph.model_validate(arch_data)

    # Load MEP graph fixture
    with open("tests/fixtures/graphs/mep_only.json") as f:
        mep_data = json.load(f)
    mep = EngineeringGraph.model_validate(mep_data)

    # Fuse
    fused, warnings = fuse_graphs(arch, mep)

    # Validate output
    assert fused.meta.title == "Demo Datacentre Architecture + Demo Datacentre MEP"
    assert fused.meta.diagram_type == "fused"

    # Ensure spaces/nodes are preserved
    assert len(fused.spaces) == 1
    assert len(fused.nodes) == 2

    # Node chiller-1 at [5.0, 5.0] should be assigned to room-1
    chiller_1 = next(n for n in fused.nodes if n.node_id == "chiller-1")
    assert chiller_1.space_id == "room-1"

    # Node chiller-2 at [15.0, 5.0] should NOT be assigned, and produce a warning
    chiller_2 = next(n for n in fused.nodes if n.node_id == "chiller-2")
    assert chiller_2.space_id is None

    assert len(warnings) == 1
    assert "chiller-2" in warnings[0]
