from fastapi.testclient import TestClient

from main import app


def test_openapi() -> None:
    with TestClient(app) as client:
        response = client.get("/openapi.json")

    assert response.status_code == 200
