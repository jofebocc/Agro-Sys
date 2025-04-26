import pytest
import uuid

@pytest.mark.asyncio
async def test_create_user(test_client):
    unique_email = f"testuser_{uuid.uuid4().hex}@example.com"
    response = test_client.post(
        "/api/v1/users/register",
        json={"email": unique_email, "password": "password123"}
    )
    print(response.status_code, response.json())

    assert response.status_code == 200
    data = response.json()
    assert "id" in data
    assert data["email"] == unique_email

@pytest.mark.asyncio
async def test_login_and_access_protected_route(test_client):
    # Step 1: Login to get token explicitly
    login_response = test_client.post(
        "/api/v1/users/login",
        data={"username": "testuser@example.com", "password": "password123"}
    )
    assert login_response.status_code == 200
    token = login_response.json()["access_token"]

    # Step 2: Access protected route explicitly
    protected_response = test_client.get(
        "/api/v1/users/me",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert protected_response.status_code == 200
    data = protected_response.json()
    assert data["email"] == "testuser@example.com"