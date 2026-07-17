from tests.helpers import (
    auth_header,
    register_user,
    login_user
)


def create_passenger(client):

    register_user(
        client,
        name="John",
        email="john@gmail.com",
        password="John@123"
    )

    return login_user(
        client,
        "john@gmail.com",
        "John@123"
    )


def test_successful_checkin(
    client,
    booking_token,
    booking_id
):

    response = client.post(
        f"/checkin/{booking_id}",
        headers=auth_header(booking_token)
    )

    assert response.status_code == 200

    assert (
        response.json()["message"]
        == "Check-in completed successfully."
    )


def test_duplicate_checkin(
    client,
    booking_token,
    booking_id
):

    client.post(
        f"/checkin/{booking_id}",
        headers=auth_header(booking_token)
    )

    response = client.post(
        f"/checkin/{booking_id}",
        headers=auth_header(booking_token)
    )

    assert response.status_code == 200

    assert (
        response.json()["message"]
        == "Passenger already checked in."
    )


def test_board_after_checkin(
    client,
    booking_token,
    booking_id
):

    client.post(
        f"/checkin/{booking_id}",
        headers=auth_header(booking_token)
    )

    response = client.post(
        f"/boarding/{booking_id}",
        headers=auth_header(booking_token),
        json={
            "gate_number": "G12"
        }
    )

    assert response.status_code == 200

    assert (
        response.json()["message"]
        == "Passenger boarded successfully."
    )


def test_board_without_checkin(
    client,
    booking_token,
    booking_id
):

    response = client.post(
        f"/boarding/{booking_id}",
        headers=auth_header(booking_token),
        json={
            "gate_number": "G10"
        }
    )

    assert response.status_code == 400


def test_duplicate_boarding(
    client,
    booking_token,
    booking_id
):

    client.post(
        f"/checkin/{booking_id}",
        headers=auth_header(booking_token)
    )

    client.post(
        f"/boarding/{booking_id}",
        headers=auth_header(booking_token),
        json={
            "gate_number": "G11"
        }
    )

    response = client.post(
        f"/boarding/{booking_id}",
        headers=auth_header(booking_token),
        json={
            "gate_number": "G11"
        }
    )

    assert response.status_code == 409


def test_cancelled_booking_cannot_checkin(
    client,
    booking_token,
    booking_id
):

    client.put(
        f"/bookings/{booking_id}",
        headers=auth_header(booking_token),
        json={
            "booking_status": "Cancelled"
        }
    )

    response = client.post(
        f"/checkin/{booking_id}",
        headers=auth_header(booking_token)
    )

    assert response.status_code == 400


def test_cancelled_booking_cannot_board(
    client,
    booking_token,
    booking_id
):

    client.put(
        f"/bookings/{booking_id}",
        headers=auth_header(booking_token),
        json={
            "booking_status": "Cancelled"
        }
    )

    response = client.post(
        f"/boarding/{booking_id}",
        headers=auth_header(booking_token),
        json={
            "gate_number": "G1"
        }
    )

    assert response.status_code == 400


def test_passenger_history(
    client,
    booking_token
):

    response = client.get(
        "/passengers/1/bookings",
        headers=auth_header(booking_token)
    )

    assert response.status_code == 200

    assert isinstance(response.json(), list)


def test_checkin_requires_login(client):

    response = client.post("/checkin/1")

    assert response.status_code == 401


def test_boarding_requires_login(client):

    response = client.post(
        "/boarding/1",
        json={
            "gate_number": "G5"
        }
    )

    assert response.status_code == 401