import pytest
import pytest_asyncio
from httpx import AsyncClient
from fastapi.testclient import TestClient
from app.main import app  # Ensure this points explicitly to your FastAPI app

@pytest.fixture(scope="module")
def test_client():
    with TestClient(app) as client:
        yield client