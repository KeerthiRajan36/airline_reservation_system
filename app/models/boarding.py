from sqlalchemy import Column,DateTime,ForeignKey,Integer,String
from sqlalchemy.orm import relationship
from datetime import datetime

from app.database.database import Base


class Boarding(Base):
    __tablename__ = "boardings"

    id = Column(Integer, primary_key=True, index=True)

    booking_id = Column(
        Integer,
        ForeignKey("bookings.id"),
        unique=True
    )

    gate_number = Column(
        String(20),
        nullable=True
    )

    boarding_time = Column(
        DateTime,
        nullable=True
    )

    boarding_status = Column(
        String(30),
        default="Pending"
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )

    booking = relationship(
        "Booking",
        back_populates="boarding"
    )