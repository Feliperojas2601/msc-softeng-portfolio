from fastapi.testclient import TestClient

from entrypoints.api.main import app

client = TestClient(app)


def test_ping_returns_pong():
    """The healthcheck endpoint answers with plain text 'pong'."""
    response = client.get("/ping")

    assert response.status_code == 200
    assert response.text == "pong"
