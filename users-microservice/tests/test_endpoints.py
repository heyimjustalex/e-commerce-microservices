import pytest
from fastapi.testclient import TestClient
from app.app import app
from app.controllers import user_controller
from app.dependencies.dependencies import get_user_service

# Create a test client for making requests to the FastAPI app
client = TestClient(app)

class MockUserService:
    def create_user(self, email: str, password: str):
        pass 

    def __call__(self):
        return self  

@pytest.fixture
def mock_user_service():
    return MockUserService()

def test_register_endpoint_override(mock_user_service):
    app.dependency_overrides[get_user_service] = mock_user_service
  
    user_data: dict[str, str] = {
        "email": "test@test.com",
        "password": "password123"
    }

    # Make a request to the register endpoint with the test data
    response = client.post("/register", json=user_data)

    # Assert the response status code
    assert response.status_code == 200

    # Assert the response content
    assert response.json() == {"message": "Registration successful. Welcome!"}
