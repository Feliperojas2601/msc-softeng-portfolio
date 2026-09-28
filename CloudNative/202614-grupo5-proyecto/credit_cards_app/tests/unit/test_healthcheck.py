from entrypoints.api.main import app


def test_ping_returns_pong():
    client = app.test_client()

    response = client.get("/credit-cards/ping")

    assert response.status_code == 200
    assert response.get_data(as_text=True) == "pong"
