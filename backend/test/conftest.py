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
