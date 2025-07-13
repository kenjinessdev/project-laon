import pytest
import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from src.main import app
from src.db.prisma import prisma  # shared Prisma instance
from unittest.mock import AsyncMock, patch, MagicMock


@pytest_asyncio.fixture(scope="function")
async def client():
    if not prisma.is_connected():
        await prisma.connect()

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac

    if prisma.is_connected():
        await prisma.disconnect()


@pytest.mark.asyncio
async def test_register_and_login(client: AsyncClient):
    test_email = "testuser@example.com"

    register_data = {
        "first_name": "Juan",
        "middle_name": "Santos",
        "last_name": "Dela Cruz",
        "suffix": "",
        "profile_image_url": "https://example.com/image.jpg",
        "email": test_email,
        "password": "securepass",
        "phone_number": "09123456789",
        "gender": "male",
        "birthday": "1990-01-01",
        "role": "farmer"
    }

    # ✅ Pre-cleanup: delete if already exists
    await prisma.user.delete_many(where={"email": test_email})

    # Register user
    response = await client.post("/api/v1/auth/register", json=register_data)
    print("REGISTER RESPONSE:", response.status_code, response.text)
    assert response.status_code == 200

    # Login
    login_data = {
        "email": test_email,
        "password": "securepass"
    }

    response = await client.post("/api/v1/auth/login", json=login_data)
    print("LOGIN RESPONSE:", response.status_code, response.text)
    assert response.status_code == 200
    assert "access_token" in response.json()

    # ✅ Post-cleanup: delete test user
    await prisma.user.delete_many(where={"email": test_email})


@pytest.mark.asyncio
async def test_invalid_login(client: AsyncClient):
    login_data = {
        "email": "wrong@example.com",
        "password": "wrongpass"
    }

    response = await client.post("/api/v1/auth/login", json=login_data)
    print("INVALID LOGIN RESPONSE:", response.status_code, response.text)
    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid credentials"


@pytest.mark.asyncio
@patch("src.core.oauth.oauth.google.get", new_callable=AsyncMock)
@patch(
    "src.core.oauth.oauth.google.authorize_access_token",
    new_callable=AsyncMock
)
async def test_mocked_google_callback(
        mock_authorize_access_token,
        mock_google_get,
        client: AsyncClient
):
    # Mock the token response
    mock_authorize_access_token.return_value = {"access_token": "fake-token"}

    # Mock the response object from oauth.google.get(...)
    mock_response = MagicMock()
    mock_response.json.return_value = {
        "names": [{"givenName": "Mock", "familyName": "User"}],
        "emailAddresses": [{"value": "mockuser@example.com"}],
        "photos": [{"url": "https://example.com/image.jpg"}],
        "birthdays": [{"date": {"year": 2000, "month": 1, "day": 1}}],
        "genders": [{"value": "male"}],
        "phoneNumbers": [{"value": "+1234567890"}]
    }
    mock_google_get.return_value = mock_response

    # Pre-cleanup
    await prisma.user.delete_many(where={"email": "mockuser@example.com"})

    # Call the callback endpoint (simulate Google redirect)
    response = await client.get("/api/v1/auth/google/callback?code=fake-code")
    assert response.status_code == 200
    json_data = response.json()
    assert "access_token" in json_data

    # Post-cleanup
    await prisma.user.delete_many(where={"email": "mockuser@example.com"})
    print(response.status_code)
    print(response.text)
