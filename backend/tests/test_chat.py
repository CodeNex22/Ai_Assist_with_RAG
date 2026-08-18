from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_chat_endpoint_rejects_empty_messages() -> None:
    response = client.post("/chat", json={"message": "   "})
    assert response.status_code == 400
