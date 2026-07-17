from sqlalchemy import Column,DateTime,Integer,String
from sqlalchemy.orm import relationship
from datetime import datetime

from app.database.database import Base


class Flight(Base):
    __tablename__ = "flights"

    id = Column(Integer, primary_key=True, index=True)

    flight_number = Column(
        String(20),
        unique=True,
        nullable=False,
        index=True
    )

    airline_name = Column(String(100), nullable=False)

    source = Column(String(100), nullable=False)

    destination = Column(String(100), nullable=False)

    departure_time = Column(DateTime, nullable=False)

    arrival_time = Column(DateTime, nullable=False)

    total_seats = Column(Integer, nullable=False)

    available_seats = Column(Integer, nullable=False)

    status = Column(
        String(20),
        default="Scheduled"
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )

    bookings = relationship(
        "Booking",
        back_populates="flight",
        cascade="all, delete"
    )