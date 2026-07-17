from tests.helpers import (
    register_user,
    login_user,
    auth_header
)


def test_register_user(client):

    response = register_user(client)

    assert response.status_code == 201

    data = response.json()

    assert data["message"] == "Registration Successful"

    assert data["user"]["email"] == "john@gmail.com"

    assert data["user"]["role"] == "Passenger"


def test_duplicate_registration(client):

    register_user(client)

    response = register_user(client)

    assert response.status_code == 409

    assert response.json()["message"] == "User already exists."


def test_login_success(client):

    register_user(client)

    response = client.post(
        "/auth/login",
        json={
            "email": "john@gmail.com",
            "password": "John@123"
        }
    )

    assert response.status_code == 200

    body = response.json()

    assert body["message"] == "Login Successful"

    assert "access_token" in body

    assert body["token_type"] == "bearer"

    assert body["role"] == "Passenger"


def test_login_invalid_password(client):

    register_user(client)

    response = client.post(
        "/auth/login",
        json={
            "email": "john@gmail.com",
            "password": "WrongPassword"
        }
    )

    assert response.status_code == 401

    assert response.json()["message"] == "Invalid email or password."


def test_login_invalid_email(client):

    response = client.post(
        "/auth/login",
        json={
            "email": "invalid@gmail.com",
            "password": "John@123"
        }
    )

    assert response.status_code == 401

    assert response.json()["message"] == "Invalid email or password."


def test_login_missing_password(client):

    register_user(client)

    response = client.post(
        "/auth/login",
        json={
            "email": "john@gmail.com"
        }
    )

    assert response.status_code == 422


def test_register_invalid_email(client):

    response = client.post(
        "/auth/register",
        json={
            "name": "John",
            "email": "invalid-email",
            "password": "John@123"
        }
    )

    assert response.status_code == 422


def test_register_short_password(client):

    response = client.post(
        "/auth/register",
        json={
            "name": "John",
            "email": "john@gmail.com",
            "password": "123"
        }
    )

    assert response.status_code == 422


def test_jwt_token_can_access_protected_route(client):

    register_user(client)

    token = login_user(
        client,
        "john@gmail.com",
        "John@123"
    )

    response = client.get(
        "/flights",
        headers=auth_header(token)
    )

    assert response.status_code == 200


def test_access_without_token(client):

    response = client.get("/flights")

    assert response.status_code == 401