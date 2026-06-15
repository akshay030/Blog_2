
from fastapi.testclient import TestClient

from src.main import app

client = TestClient(app)


def test_register_invalid_email():

    response = client.post(
        "/user/register",
        json={
            "username": "akshay",
            "email": "invalid-email",
            "password": "123456"
        }
    )

    assert response.status_code == 422
    
def test_login_missing_password():

    response = client.post(
        "/user/login",
        json={
            "email": "test@test.com"
        }
    )

    assert response.status_code == 422