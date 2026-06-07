import io
import json

import pytest
from fastapi.testclient import TestClient

from app.main import build_app
from app.schemas import EngineeringGraph


@pytest.fixture
def client():
    app = build_app()
    return TestClient(app)


def test_demo_floorplan(client: TestClient):
    response = client.get("/api/demo/floorplan")
    assert response.status_code == 200
    data = response.json()
    assert "spaces" in data
    # Ensure it maps to the correct schema
    EngineeringGraph.model_validate(data)


def test_demo_compliance_graph(client: TestClient):
    response = client.get("/api/demo/compliance-graph")
    assert response.status_code == 200
    data = response.json()
    assert "nodes" in data
    EngineeringGraph.model_validate(data)


def test_demo_compliance_report(client: TestClient):
    response = client.get("/api/demo/compliance-report")
    assert response.status_code == 200
    data = response.json()
    assert "checks_run" in data
    assert "violations" in data


def test_overlay_valid_payload(client: TestClient):
    # Create a minimal valid JPEG image
    from PIL import Image

    img = Image.new("RGB", (100, 100), color="white")
    img_bytes = io.BytesIO()
    img.save(img_bytes, format="JPEG")
    img_bytes.seek(0)

    # Create a minimal valid graph
    graph_data = {
        "meta": {"diagram_type": "FUSED"},
        "nodes": [{"node_id": "n1", "position": [50, 50]}],
        "spaces": [{"space_id": "s1", "polygon": [[10, 10], [90, 10], [90, 90], [10, 90]]}],
    }

    files = {"image": ("test.jpg", img_bytes, "image/jpeg")}
    data = {"graph": json.dumps(graph_data)}

    response = client.post("/api/overlay", files=files, data=data)
    assert response.status_code == 200
    assert response.headers["content-type"] == "image/jpeg"
    assert len(response.content) > 0


def test_overlay_invalid_graph(client: TestClient):
    from PIL import Image

    img = Image.new("RGB", (100, 100), color="white")
    img_bytes = io.BytesIO()
    img.save(img_bytes, format="JPEG")
    img_bytes.seek(0)

    files = {"image": ("test.jpg", img_bytes, "image/jpeg")}
    data = {"graph": '{"invalid": "graph"}'}

    response = client.post("/api/overlay", files=files, data=data)
    assert response.status_code == 400
    assert "Invalid graph payload" in response.text


def test_overlay_invalid_image(client: TestClient):
    graph_data = {"meta": {"diagram_type": "FUSED"}, "nodes": []}

    files = {"image": ("test.txt", io.BytesIO(b"not an image"), "text/plain")}
    data = {"graph": json.dumps(graph_data)}

    response = client.post("/api/overlay", files=files, data=data)
    assert response.status_code == 400
    assert "Invalid image payload" in response.text
