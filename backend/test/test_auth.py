import pytest
import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from src.main import app
from src.db.prisma import prisma  # shared Prisma instance


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
    response = await client.post("/auth/register", json=register_data)
    print("REGISTER RESPONSE:", response.status_code, response.text)
    assert response.status_code == 200

    # Login
    login_data = {
        "email": test_email,
        "password": "securepass"
    }

    response = await client.post("/auth/login", json=login_data)
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

    response = await client.post("/auth/login", json=login_data)
    print("INVALID LOGIN RESPONSE:", response.status_code, response.text)
    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid credentials"

