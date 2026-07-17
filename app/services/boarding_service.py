from datetime import datetime, timedelta

from sqlalchemy.orm import Session

from app.models.booking import Booking
from app.models.boarding import Boarding
from app.models.user import User

from app.exceptions.custom_exceptions import (
    BookingNotFoundException,
    BookingCancelledException,
    CheckInNotAllowedException,
    BoardingNotAllowedException,
    BoardingAlreadyCompletedException,
    ForbiddenException
)


class BoardingService:

    @staticmethod
    def check_in(
        db: Session,
        booking_id: int,
        current_user: User
    ):

        booking = (
            db.query(Booking)
            .filter(Booking.id == booking_id)
            .first()
        )

        if not booking:
            raise BookingNotFoundException()

        if (
            current_user.role == "Passenger"
            and booking.passenger_id != current_user.id
        ):
            raise ForbiddenException()

        if booking.booking_status == "Cancelled":
            raise BookingCancelledException()

        departure_time = booking.flight.departure_time

        now = datetime.utcnow()

        checkin_start = departure_time - timedelta(hours=24)

        if not (checkin_start <= now <= departure_time):
            raise CheckInNotAllowedException()

        if booking.checked_in:
            return {
                "message": "Passenger already checked in."
            }

        booking.checked_in = True
        booking.booking_status = "Confirmed"

        db.commit()
        db.refresh(booking)

        return {
            "message": "Check-in completed successfully.",
            "data": booking
        }

    @staticmethod
    def board_passenger(
        db: Session,
        booking_id: int,
        gate_number: str,
        current_user: User
    ):

        booking = (
            db.query(Booking)
            .filter(Booking.id == booking_id)
            .first()
        )

        if not booking:
            raise BookingNotFoundException()

        if (
            current_user.role == "Passenger"
            and booking.passenger_id != current_user.id
        ):
            raise ForbiddenException()

        if booking.booking_status == "Cancelled":
            raise BookingCancelledException()

        if not booking.checked_in:
            raise BoardingNotAllowedException()

        if booking.boarded:
            raise BoardingAlreadyCompletedException()

        boarding = (
            db.query(Boarding)
            .filter(
                Boarding.booking_id == booking.id
            )
            .first()
        )

        if boarding:

            boarding.gate_number = gate_number
            boarding.boarding_time = datetime.utcnow()
            boarding.boarding_status = "Boarded"

        else:

            boarding = Boarding(
                booking_id=booking.id,
                gate_number=gate_number,
                boarding_time=datetime.utcnow(),
                boarding_status="Boarded"
            )

            db.add(boarding)

        booking.boarded = True
        booking.booking_status = "Completed"

        db.commit()
        db.refresh(boarding)

        return {
            "message": "Passenger boarded successfully.",
            "data": boarding
        }

    @staticmethod
    def get_passenger_history(
        db: Session,
        passenger_id: int,
        current_user: User
    ):

        if (
            current_user.role == "Passenger"
            and passenger_id != current_user.id
        ):
            raise ForbiddenException()

        bookings = (
            db.query(Booking)
            .filter(
                Booking.passenger_id == passenger_id
            )
            .all()
        )

        return bookings