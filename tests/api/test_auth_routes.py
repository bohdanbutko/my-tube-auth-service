from uuid import uuid4

import pytest
from fastapi.testclient import TestClient

from src.api.server import app
from src.infrastructure.repositories import InMemoryIdentityRepository


client = TestClient(app)


@pytest.fixture(autouse=True)
def clear_repository(monkeypatch):
    monkeypatch.setenv("JWT_SECRET_KEY", "test-secret-key-with-at-least-32-bytes")
    monkeypatch.setenv("JWT_ALGORITHM", "HS256")
    InMemoryIdentityRepository().clear()


def test_health_returns_ok():
    response = client.get("/api/v1/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_provision_login_and_verify_token_flow():
    subject_id = str(uuid4())
    channel_id = str(uuid4())
    provision_response = client.post(
        "/api/v1/identities",
        json={
            "subject_id": subject_id,
            "email": "test@example.com",
            "password": "password",
            "channel_accesses": [{"channel_id": channel_id, "role": "channel_viewer"}],
        },
    )
    assert provision_response.status_code == 201

    login_response = client.post(
        "/api/v1/login",
        data={"username": "test@example.com", "password": "password"},
    )
    assert login_response.status_code == 200
    token = login_response.json()["access_token"]

    verify_response = client.get(
        "/api/v1/verify-token",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert verify_response.status_code == 200
    payload = verify_response.json()["data"]
    assert payload["sub"] == subject_id
    assert payload["channels"] == [
        {
            "channel_id": channel_id,
            "role": "channel_viewer",
            "permissions": [
                "channel:view",
                "analytics:view_revenue",
                "live_stream:view",
            ],
        }
    ]


def test_provision_duplicate_identity_returns_conflict():
    subject_id = str(uuid4())
    channel_id = str(uuid4())
    payload = {
        "subject_id": subject_id,
        "email": "test@example.com",
        "password": "password",
        "channel_accesses": [{"channel_id": channel_id, "role": "channel_viewer"}],
    }

    assert client.post("/api/v1/identities", json=payload).status_code == 201
    assert client.post("/api/v1/identities", json=payload).status_code == 409


def test_provision_unknown_role_returns_bad_request():
    response = client.post(
        "/api/v1/identities",
        json={
            "subject_id": str(uuid4()),
            "email": "test@example.com",
            "password": "password",
            "channel_accesses": [{"channel_id": str(uuid4()), "role": "missing-role"}],
        },
    )

    assert response.status_code == 400
