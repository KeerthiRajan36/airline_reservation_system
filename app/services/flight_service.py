from sqlalchemy.orm import Session
from sqlalchemy import or_

from app.models.flight import Flight
from app.schemas.flight_schema import (
    FlightCreate,
    FlightUpdate
)

from app.exceptions.custom_exceptions import (
    FlightAlreadyExistsException,
    FlightNotFoundException
)


class FlightService:

    @staticmethod
    def create_flight(
        db: Session,
        request: FlightCreate
    ):

        flight = (
            db.query(Flight)
            .filter(
                Flight.flight_number == request.flight_number
            )
            .first()
        )

        if flight:
            raise FlightAlreadyExistsException()

        new_flight = Flight(
            flight_number=request.flight_number,
            airline_name=request.airline_name,
            source=request.source,
            destination=request.destination,
            departure_time=request.departure_time,
            arrival_time=request.arrival_time,
            total_seats=request.total_seats,
            available_seats=request.total_seats,
            status="Scheduled"
        )

        db.add(new_flight)
        db.commit()
        db.refresh(new_flight)

        return {
            "message": "Flight Created Successfully",
            "data": new_flight
        }

    @staticmethod
    def get_all_flights(
        db: Session,
        page: int,
        limit: int
    ):

        offset = (page - 1) * limit

        flights = (
            db.query(Flight)
            .offset(offset)
            .limit(limit)
            .all()
        )

        total = db.query(Flight).count()

        return {
            "page": page,
            "limit": limit,
            "total": total,
            "data": flights
        }

    @staticmethod
    def get_flight_by_id(
        db: Session,
        flight_id: int
    ):

        flight = (
            db.query(Flight)
            .filter(
                Flight.id == flight_id
            )
            .first()
        )

        if not flight:
            raise FlightNotFoundException()

        return flight

    @staticmethod
    def update_flight(
        db: Session,
        flight_id: int,
        request: FlightUpdate
    ):

        flight = (
            db.query(Flight)
            .filter(
                Flight.id == flight_id
            )
            .first()
        )

        if not flight:
            raise FlightNotFoundException()

        update_data = request.model_dump(
            exclude_unset=True
        )

        if "total_seats" in update_data:

            booked = (
                flight.total_seats -
                flight.available_seats
            )

            if update_data["total_seats"] < booked:

                raise ValueError(
                    "Total seats cannot be less than booked seats."
                )

            flight.available_seats = (
                update_data["total_seats"] -
                booked
            )

        for key, value in update_data.items():
            setattr(flight, key, value)

        db.commit()
        db.refresh(flight)

        return {
            "message": "Flight Updated Successfully",
            "data": flight
        }

    @staticmethod
    def delete_flight(
        db: Session,
        flight_id: int
    ):

        flight = (
            db.query(Flight)
            .filter(
                Flight.id == flight_id
            )
            .first()
        )

        if not flight:
            raise FlightNotFoundException()

        db.delete(flight)
        db.commit()

        return {
            "message": "Flight Deleted Successfully"
        }

    @staticmethod
    def search_flights(
        db: Session,
        source: str,
        destination: str,
        page: int,
        limit: int
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
            query.offset((page - 1) * limit)
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
    def get_available_flights(
        db: Session
    ):

        return (
            db.query(Flight)
            .filter(
                Flight.available_seats > 0,
                Flight.status == "Scheduled"
            )
            .all()
        )