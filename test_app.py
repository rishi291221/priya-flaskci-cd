import os

# Provide test environment variables before importing the Flask app.
os.environ["MONGO_URI"] = "mongodb://localhost:27017/test"
os.environ["SECRET_KEY"] = "test-secret"

from app import app, mongo


def test_health(monkeypatch):
    """Test that /health returns HTTP 200 when MongoDB is reachable."""

    class FakeAdmin:
        def command(self, command):
            assert command == "ping"
            return {"ok": 1}

    class FakeClient:
        admin = FakeAdmin()

    # Replace the real MongoDB client with our fake client.
    monkeypatch.setattr(mongo, "cx", FakeClient())

    client = app.test_client()

    response = client.get("/health")

    assert response.status_code == 200

    data = response.get_json()

    assert data["status"] == "healthy"
    assert data["mongodb"] == "connected"
