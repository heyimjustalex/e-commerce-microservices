import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))
from app.app import *
import pytest
from fastapi.testclient import TestClient

@pytest.fixture
def client() -> TestClient:
    return TestClient(app)

def test_register_success(client):
    # Given
    user_data : dict = {"email":"aaa@aaa.com","password":"pass123d"}

    # When
    response = client.post("/register", json=user_data)

    # Then
    assert response.status_code == 200
    assert response.json() == {"message": "Registration successful. Welcome!"}
