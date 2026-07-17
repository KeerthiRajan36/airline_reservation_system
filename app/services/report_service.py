from sqlalchemy.orm import Session
from sqlalchemy import func

from app.models.flight import Flight
from app.models.booking import Booking
from app.models.user import User

from app.exceptions.custom_exceptions import (
    InvalidStatusException
)

from app.utils.validator import validate_booking_status


class ReportService:

    @staticmethod
    def search_flights(
        db: Session,
        source: str = None,
        destination: str = None,
        page: int = 1,
        limit: int = 10
    ):

        query = db.query(Flight)

        if source:
            query = query.filter(
                Flight.source.ilike(f"%{source}%")
            )

        if destination:
            query = query.filter(
                Flight.destination.ilike(f"%{destination}%")
            )

        total = query.count()

        flights = (
            query
            .offset((page - 1) * limit)
            .limit(limit)
            .all()
        )

        return {
            "page": page,
            "limit": limit,
            "total": total,
            "data": flights
        }

    @staticmethod
    def bookings_by_status(
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
            query
            .offset((page - 1) * limit)
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
    def passenger_history(
        db: Session,
        passenger_id: int
    ):

        return (
            db.query(Booking)
            .filter(
                Booking.passenger_id == passenger_id
            )
            .order_by(
                Booking.created_at.desc()
            )
            .all()
        )

    @staticmethod
    def dashboard(db: Session):

        total_flights = db.query(Flight).count()

        total_passengers = (
            db.query(User)
            .filter(
                User.role == "Passenger"
            )
            .count()
        )

        total_bookings = db.query(Booking).count()

        booked = (
            db.query(Booking)
            .filter(
                Booking.booking_status == "Booked"
            )
            .count()
        )

        confirmed = (
            db.query(Booking)
            .filter(
                Booking.booking_status == "Confirmed"
            )
            .count()
        )

        completed = (
            db.query(Booking)
            .filter(
                Booking.booking_status == "Completed"
            )
            .count()
        )

        cancelled = (
            db.query(Booking)
            .filter(
                Booking.booking_status == "Cancelled"
            )
            .count()
        )

        available_seats = (
            db.query(
                func.sum(
                    Flight.available_seats
                )
            )
            .scalar()
        ) or 0

        total_seats = (
            db.query(
                func.sum(
                    Flight.total_seats
                )
            )
            .scalar()
        ) or 0

        return {

            "total_flights": total_flights,

            "total_passengers": total_passengers,

            "total_bookings": total_bookings,

            "booking_summary": {

                "booked": booked,

                "confirmed": confirmed,

                "completed": completed,

                "cancelled": cancelled

            },

            "total_seats": total_seats,

            "available_seats": available_seats,

            "occupied_seats": total_seats - available_seats

        }

    @staticmethod
    def flight_statistics(db: Session):

        flights = db.query(Flight).all()

        result = []

        for flight in flights:

            booked = (
                flight.total_seats -
                flight.available_seats
            )

            result.append({

                "flight_id": flight.id,

                "flight_number": flight.flight_number,

                "airline": flight.airline_name,

                "route": f"{flight.source} -> {flight.destination}",

                "total_seats": flight.total_seats,

                "available_seats": flight.available_seats,

                "booked_seats": booked,

                "occupancy_percentage":
                    round(
                        booked / flight.total_seats * 100,
                        2
                    )

            })

        return result