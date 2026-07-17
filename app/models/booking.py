from sqlalchemy import Boolean, Column, Date, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from datetime import datetime

from app.database.database import Base


class Booking(Base):
    __tablename__ = "bookings"

    id = Column(Integer, primary_key=True, index=True)

    booking_reference = Column(
        String(30),
        unique=True,
        nullable=False
    )

    passenger_id = Column(
        Integer,
        ForeignKey("users.id")
    )

    flight_id = Column(
        Integer,
        ForeignKey("flights.id")
    )

    journey_date = Column(
        Date,
        nullable=False
    )

    seat_number = Column(
        String(10),
        nullable=False
    )

    booking_status = Column(
        String(20),
        default="Booked"
    )

    checked_in = Column(
        Boolean,
        default=False
    )

    boarded = Column(
        Boolean,
        default=False
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )

    passenger = relationship(
        "User",
        back_populates="bookings"
    )

    flight = relationship(
        "Flight",
        back_populates="bookings"
    )

    boarding = relationship(
        "Boarding",
        back_populates="booking",
        uselist=False,
        cascade="all, delete"
    )