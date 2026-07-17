from datetime import date


def validate_journey_date(
        journey_date: date
):

    if journey_date < date.today():
        return False

    return True


def validate_booking_status(
        status: str
):

    allowed = [
        "Booked",
        "Confirmed",
        "Cancelled",
        "Completed"
    ]

    return status in allowed


def validate_seat_number(
        seat: str
):

    if len(seat) < 2:
        return False

    return True