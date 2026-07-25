from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_health_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_audit_endpoint():
    response = client.post(
        "/audit",
        json={"url": "https://example.com"},
    )
    assert response.status_code == 200
    body = response.json()
    assert body["url"] == "https://example.com"
    assert body["result"]["is_valid"] is True
    assert body["result"]["domain"] == "example.com"
