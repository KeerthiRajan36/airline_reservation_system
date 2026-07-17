import uuid
from datetime import date

from sqlalchemy.orm import Session

from app.models.booking import Booking
from app.models.flight import Flight
from app.models.user import User

from app.schemas.booking_schema import (
    BookingCreate,
    BookingUpdate
)

from app.exceptions.custom_exceptions import (
    BookingNotFoundException,
    FlightNotFoundException,
    FlightCapacityException,
    SeatAlreadyBookedException,
    JourneyDateException,
    PassengerNotFoundException,
    InvalidStatusException,
)

from app.utils.validator import (
    validate_journey_date,
    validate_booking_status,
)


class BookingService:

    @staticmethod
    def create_booking(
        db: Session,
        current_user: User,
        request: BookingCreate
    ):

        # Journey date validation
        if not validate_journey_date(request.journey_date):
            raise JourneyDateException()

        # Flight validation
        flight = (
            db.query(Flight)
            .filter(Flight.id == request.flight_id)
            .first()
        )

        if not flight:
            raise FlightNotFoundException()

        # Seat availability
        if flight.available_seats <= 0:
            raise FlightCapacityException()

        # Duplicate seat validation
        seat = (
            db.query(Booking)
            .filter(
                Booking.flight_id == request.flight_id,
                Booking.journey_date == request.journey_date,
                Booking.seat_number == request.seat_number,
                Booking.booking_status != "Cancelled"
            )
            .first()
        )

        if seat:
            raise SeatAlreadyBookedException()

        booking = Booking(
            booking_reference=str(uuid.uuid4())[:8].upper(),
            passenger_id=current_user.id,
            flight_id=request.flight_id,
            journey_date=request.journey_date,
            seat_number=request.seat_number,
            booking_status="Booked",
            checked_in=False,
            boarded=False
        )

        db.add(booking)

        flight.available_seats -= 1

        db.commit()
        db.refresh(booking)

        return {
            "message": "Booking Successful",
            "data": booking
        }

    @staticmethod
    def get_all_bookings(db, current_user, page, limit):
        query = db.query(Booking)

        if current_user.role == "Passenger":
            query = query.filter(
                Booking.passenger_id == current_user.id
            )

        total = query.count()

        bookings = (
            query.offset((page - 1) * limit)
            .limit(limit)
            .all()
        )

        return {
            "page": page,
            "limit": limit,
            "total": total,
            "data": bookings
        }

    @staticmethod
    def get_booking_by_id(
        db: Session,
        booking_id: int
    ):

        booking = (
            db.query(Booking)
            .filter(Booking.id == booking_id)
            .first()
        )

        if not booking:
            raise BookingNotFoundException()

        return booking

    @staticmethod
    def update_booking(
        db: Session,
        booking_id: int,
        request: BookingUpdate
    ):

        booking = (
            db.query(Booking)
            .filter(Booking.id == booking_id)
            .first()
        )

        if not booking:
            raise BookingNotFoundException()

        update_data = request.model_dump(
            exclude_unset=True
        )

        # Seat change validation
        if "seat_number" in update_data:

            seat_exists = (
                db.query(Booking)
                .filter(
                    Booking.flight_id == booking.flight_id,
                    Booking.journey_date == booking.journey_date,
                    Booking.seat_number == update_data["seat_number"],
                    Booking.id != booking.id,
                    Booking.booking_status != "Cancelled"
                )
                .first()
            )

            if seat_exists:
                raise SeatAlreadyBookedException()

            booking.seat_number = update_data["seat_number"]

        # Booking status update
        if "booking_status" in update_data:

            status = update_data["booking_status"]

            if not validate_booking_status(status):
                raise InvalidStatusException()

            if (
                booking.booking_status != "Cancelled"
                and status == "Cancelled"
            ):
                flight = (
                    db.query(Flight)
                    .filter(Flight.id == booking.flight_id)
                    .first()
                )

                flight.available_seats += 1

            booking.booking_status = status

        db.commit()
        db.refresh(booking)

        return {
            "message": "Booking Updated Successfully",
            "data": booking
        }

    @staticmethod
    def get_passenger_bookings(
        db: Session,
        passenger_id: int
    ):

        passenger = (
            db.query(User)
            .filter(User.id == passenger_id)
            .first()
        )

        if not passenger:
            raise PassengerNotFoundException()

        return (
            db.query(Booking)
            .filter(
                Booking.passenger_id == passenger_id
            )
            .all()
        )

    @staticmethod
    def filter_bookings_by_status(
        db: Session,
        status: str,
        page: int,
        limit: int
    ):

        if not validate_booking_status(status):
            raise InvalidStatusException()

        query = (
            db.query(Booking)
            .filter(
                Booking.booking_status == status
            )
        )

        total = query.count()

        bookings = (
            query.offset((page - 1) * limit)
            .limit(limit)
            .all()
        )

        return {
            "page": page,
            "limit": limit,
            "total": total,
            "data": bookings
        }