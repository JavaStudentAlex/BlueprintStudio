import pytest

from app.schemas import EngineeringGraph, GraphMeta, GraphSpace
from app.services.property_valuation import calculate_property_valuation, derive_total_area


def test_derive_total_area_from_meta():
    graph = EngineeringGraph(meta=GraphMeta(properties={"total_area": 150.5}))
    assert derive_total_area(graph) == 150.5


def test_derive_total_area_from_spaces():
    graph = EngineeringGraph(
        spaces=[
            GraphSpace(space_id="s1", area=50.0),
            GraphSpace(space_id="s2", area=25.5),
            GraphSpace(space_id="s3", area=None),
        ]
    )
    assert derive_total_area(graph) == 75.5


def test_calculate_property_valuation_success():
    graph = EngineeringGraph(spaces=[GraphSpace(space_id="s1", area=100.0)])
    # Using Kwun Tong mock: price=80000.0, rent=300.0
    res = calculate_property_valuation(graph, "Kwun Tong")

    assert res.total_area_sqm == 100.0
    assert res.estimated_value_hkd == 8000000.0
    assert res.estimated_monthly_rent_hkd == 30000.0

    # ROI = (30000 * 12) / 8000000 * 100 = 360000 / 8000000 * 100 = 4.5
    assert res.estimated_roi_percentage == 4.5
    assert "Dataset" in res.dataset_provenance


def test_calculate_property_valuation_unknown_district():
    graph = EngineeringGraph(meta=GraphMeta(properties={"total_area": 100.0}))
    with pytest.raises(ValueError, match="Unknown district: Unknown"):
        calculate_property_valuation(graph, "Unknown")


def test_calculate_property_valuation_zero_area():
    graph = EngineeringGraph()
    with pytest.raises(ValueError, match="Total area could not be derived"):
        calculate_property_valuation(graph, "Central")
