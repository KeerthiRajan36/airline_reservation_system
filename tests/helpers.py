def register_user(
    client,
    name="John",
    email="john@gmail.com",
    password="John@123"
):

    return client.post(
        "/auth/register",
        json={
            "name": name,
            "email": email,
            "password": password
        }
    )


def login_user(
    client,
    email,
    password
):

    response = client.post(
        "/auth/login",
        json={
            "email": email,
            "password": password
        }
    )

    return response.json()["access_token"]


def auth_header(token):

    return {
        "Authorization": f"Bearer {token}"
    }