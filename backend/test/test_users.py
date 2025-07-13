from prisma.errors import UniqueViolationError
import pytest
import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from src.main import app
from src.db.prisma import prisma
from src.utils.jwt import create_access_token
from datetime import datetime


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
async def test_update_user_profile(client):  # Use the fixture here
    # Create a test user
    user = await prisma.user.create({
        "first_name": "Old",
        "middle_name": "Test",
        "last_name": "User",
        "email": "testuser@example.com",
        "password": "hashed_password",
        "phone_number": "09123456789",
        "gender": "male",
        "birthday": datetime(1990, 1, 1),
        "role": "customer",
        "profile_image_url": "",
        "suffix": "",
    })

    access_token = create_access_token(user.id)

    update_data = {
        "first_name": "Updated",
        "last_name": "Name",
    }

    response = await client.put(
        "/api/v1/users/me",
        json=update_data,
        headers={"Authorization": f"Bearer {access_token}"}
    )

    assert response.status_code == 200
    json_data = response.json()
    assert json_data["first_name"] == "Updated"
    assert json_data["last_name"] == "Name"

    await prisma.user.delete(where={"id": user.id})


@pytest.mark.asyncio
async def test_update_profile_email_or_phone_conflict(client):
    # Create User A (will attempt to update to User B's email/phone)
    user_a = await prisma.user.create({
        "first_name": "User",
        "last_name": "A",
        "email": "usera@example.com",
        "password": "hashed_password",
        "phone_number": "test_number",
        "gender": "male",
        "birthday": datetime(1990, 1, 1),
        "role": "customer",
        "profile_image_url": "",
        "suffix": "",
        "middle_name": ""
    })

    # Create User B (owns the conflicting email/phone)
    user_b = await prisma.user.create({
        "first_name": "User",
        "last_name": "B",
        "email": "userb@example.com",
        "password": "hashed_password",
        "phone_number": "test_number2",
        "gender": "female",
        "birthday": datetime(1990, 1, 1),
        "role": "customer",
        "profile_image_url": "",
        "suffix": "",
        "middle_name": ""
    })

    # Generate token for User A
    access_token = create_access_token(user_a.id)

    # Test conflicting email
    response = await client.put(
        "/api/v1/users/me",
        json={"email": "userb@example.com"},
        headers={"Authorization": f"Bearer {access_token}"}
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "Email is already registered."
    # assert "Email already registered" in response.text

    # Test conflicting phone number
    response = await client.put(
        "/api/v1/users/me",
        json={"phone_number": "test_number2"},
        headers={"Authorization": f"Bearer {access_token}"}
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "Phone number is already registered."
    # assert "Phone number already registered" in response.text

    # Clean up
    await prisma.user.delete(where={"id": user_a.id})
    await prisma.user.delete(where={"id": user_b.id})
