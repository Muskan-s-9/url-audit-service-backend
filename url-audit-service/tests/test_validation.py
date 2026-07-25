from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_invalid_url_rejected():
    response = client.post(
        "/audit",
        json={"url": "not-a-url"},
    )
    assert response.status_code == 422
    assert response.json()["error"] == "validation_error"


def test_empty_url_rejected():
    response = client.post(
        "/audit",
        json={"url": "   "},
    )
    assert response.status_code == 422
