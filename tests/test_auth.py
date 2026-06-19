def test_register_missing_name_returns_validation_error(client):

    response = client.post(
        "/user/register",
        json={
            "username": "akshay",
            "email": "invalid-email",
            "password": "123456"
        }
    )

    assert response.status_code == 422
    
def test_login_missing_password_returns_validation_error(client):

    response = client.post(
        "/user/login",
        json={
            "email": "test@test.com"
        }
    )

    assert response.status_code == 422


def test_login_returns_token_for_valid_credentials(client, monkeypatch, fake_user):
    token = "test-token"

    def fake_login(body, db):
        return {
            "access_token": token,
            "token_type": "bearer",
            "user": fake_user,
        }

    monkeypatch.setattr("src.users.controllers.login", fake_login)

    response = client.post(
        "/user/login",
        json={
            "email": fake_user.email,
            "password": "password123",
        },
    )

    assert response.status_code == 200
    assert response.json()["access_token"] == token
    assert response.json()["token_type"] == "bearer"
