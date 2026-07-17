from tests.helpers import register_user, login_user, auth_header


def create_flight(client, admin_token):

    response = client.post(
        "/flights",
        headers=auth_header(admin_token),
        json={
            "flight_number": "AI101",
            "airline_name": "Air India",
            "source": "Chennai",
            "destination": "Delhi",
            "departure_time": "2026-08-20T09:00:00",
            "arrival_time": "2026-08-20T11:30:00",
            "total_seats": 2
        }
    )

    return response.json()["data"]["id"]


def create_passenger(client):

    register_user(
        client,
        name="John",
        email="john@gmail.com",
        password="John@123"
    )

    token = login_user(
        client,
        "john@gmail.com",
        "John@123"
    )

    return token


def booking_payload(flight_id):

    return {
        "flight_id": flight_id,
        "journey_date": "2026-08-20",
        "seat_number": "12A"
    }


def test_create_booking(client, admin_token):

    flight_id = create_flight(client, admin_token)

    passenger_token = create_passenger(client)

    response = client.post(
        "/bookings",
        headers=auth_header(passenger_token),
        json=booking_payload(flight_id)
    )

    assert response.status_code == 201

    assert response.json()["message"] == "Booking Successful"


def test_duplicate_seat_booking(client, admin_token):

    flight_id = create_flight(client, admin_token)

    passenger_token = create_passenger(client)

    client.post(
        "/bookings",
        headers=auth_header(passenger_token),
        json=booking_payload(flight_id)
    )

    response = client.post(
        "/bookings",
        headers=auth_header(passenger_token),
        json=booking_payload(flight_id)
    )

    assert response.status_code == 409


def test_booking_with_past_date(client, admin_token):

    flight_id = create_flight(client, admin_token)

    passenger_token = create_passenger(client)

    response = client.post(
        "/bookings",
        headers=auth_header(passenger_token),
        json={
            "flight_id": flight_id,
            "journey_date": "2025-01-01",
            "seat_number": "14A"
        }
    )

    assert response.status_code == 400


def test_change_seat(client, admin_token):

    flight_id = create_flight(client, admin_token)

    passenger_token = create_passenger(client)

    client.post(
        "/bookings",
        headers=auth_header(passenger_token),
        json=booking_payload(flight_id)
    )

    response = client.put(
        "/bookings/1",
        headers=auth_header(passenger_token),
        json={
            "seat_number": "15C"
        }
    )

    assert response.status_code == 200

    assert response.json()["data"]["seat_number"] == "15C"


def test_cancel_booking(client, admin_token):

    flight_id = create_flight(client, admin_token)

    passenger_token = create_passenger(client)

    client.post(
        "/bookings",
        headers=auth_header(passenger_token),
        json=booking_payload(flight_id)
    )

    response = client.put(
        "/bookings/1",
        headers=auth_header(passenger_token),
        json={
            "booking_status": "Cancelled"
        }
    )

    assert response.status_code == 200

    assert (
        response.json()["data"]["booking_status"]
        == "Cancelled"
    )


def test_get_booking(client, admin_token):

    flight_id = create_flight(client, admin_token)

    passenger_token = create_passenger(client)

    client.post(
        "/bookings",
        headers=auth_header(passenger_token),
        json=booking_payload(flight_id)
    )

    response = client.get(
        "/bookings/1",
        headers=auth_header(passenger_token)
    )

    assert response.status_code == 200


def test_get_all_bookings(client, admin_token):

    passenger_token = create_passenger(client)

    response = client.get(
        "/bookings",
        headers=auth_header(passenger_token)
    )

    assert response.status_code == 200


def test_booking_not_found(client):

    response = client.get(
        "/bookings/999",
        headers={
            "Authorization": "Bearer invalid"
        }
    )

    assert response.status_code in [401, 404]


def test_booking_requires_login(client):

    response = client.get("/bookings")

    assert response.status_code == 401