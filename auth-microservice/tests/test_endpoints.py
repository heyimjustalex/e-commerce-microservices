import pytest
from fastapi.testclient import TestClient
from fastapi import status
from app.app import app
from app.controllers import auth_controller
from app.dependencies.dependencies import get_user_service
from app.exceptions.definitions import UserAlreadyExists, UserEmailIncorrectFormat, UserInvalidCredentials
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

def test_register_endpoint_when_correct_credentials(mock_user_service):
    app.dependency_overrides[get_user_service] = mock_user_service
  
    user_data: dict[str, str] = {
        "email": "test@test.com",
        "password": "password123"
    }
    response = client.post("/api/auth/register", json=user_data)

    assert response.status_code == status.HTTP_201_CREATED    
 

def test_register_endpoint_when_user_already_exists(mock_user_service):
    app.dependency_overrides[get_user_service] = mock_user_service
  
    def create_user_with_existing_email(email, password):
        raise UserAlreadyExists()
    
    mock_user_service.create_user = create_user_with_existing_email

    user_data: dict[str, str] = {
        "email": "test@test.com",
        "password": "password123"
    }
    response = client.post("/api/auth/register", json=user_data)

    assert response.status_code == status.HTTP_400_BAD_REQUEST    


def test_register_endpoint_when_invalid_email_format(mock_user_service):
    app.dependency_overrides[get_user_service] = mock_user_service
  
    user_data: dict[str, str] = {
        "email": "test@test.com",
        "password": "password123"
    }
  
    # Mock the UserService.create_user method to raise UserEmailIncorrectFormat exception
    def create_user_with_invalid_email(email, password):
        raise UserEmailIncorrectFormat()

    mock_user_service.create_user = create_user_with_invalid_email

    response = client.post("/api/auth/register", json=user_data)

    assert response.status_code == status.HTTP_400_BAD_REQUEST


