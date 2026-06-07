from fastapi.testclient import TestClient


def test_property_valuation_success(client: TestClient):
    payload = {"graph": {"meta": {"properties": {"total_area": 100.0}}}, "district": "Central"}

    response = client.post("/api/finance/property/valuation", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["total_area_sqm"] == 100.0
    assert data["estimated_value_hkd"] == 20000000.0
    assert data["estimated_monthly_rent_hkd"] == 80000.0


def test_property_valuation_unknown_district(client: TestClient):
    payload = {"graph": {"meta": {"properties": {"total_area": 100.0}}}, "district": "Unknown"}

    response = client.post("/api/finance/property/valuation", json=payload)
    assert response.status_code == 422
    assert "Unknown district: Unknown" in response.json()["detail"]


def test_property_valuation_zero_area(client: TestClient):
    payload = {"graph": {}, "district": "Central"}

    response = client.post("/api/finance/property/valuation", json=payload)
    assert response.status_code == 422
    assert "Total area could not be derived" in response.json()["detail"]
