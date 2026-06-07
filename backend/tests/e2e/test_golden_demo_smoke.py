import pytest
from fastapi.testclient import TestClient


@pytest.mark.asyncio
async def test_golden_demo_smoke(app_with_fakes):
    """
    Smoke test to prove that the backend demo routes (e.g., finance valuation, etc.)
    can be reached without external services, utilizing committed fixtures.
    """
    with TestClient(app_with_fakes) as client:
        # Check health
        resp = client.get("/health")
        assert resp.status_code == 200

        # Check ready status
        resp = client.get("/ready")
        assert resp.status_code == 200

        # Test the finance valuation demo route with a synthetic payload
        # This payload matches what frontend sends or what the service expects
        req_payload = {
            "graph": {
                "nodes": [
                    {"id": "space-1", "type": "space", "properties": {"area": 100, "use": "office"}}
                ],
                "edges": [],
            },
            "district": "financial",
        }
        resp = client.post("/api/finance/property/valuation", json=req_payload)
        assert resp.status_code in (200, 422)  # Should return validation or success, not 500
