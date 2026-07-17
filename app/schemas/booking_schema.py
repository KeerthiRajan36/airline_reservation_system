from datetime import date
from datetime import datetime

from pydantic import BaseModel
from pydantic import Field


class BookingCreate(BaseModel):

    flight_id: int

    journey_date: date

    seat_number: str = Field(..., example="12A")


class BookingUpdate(BaseModel):

    seat_number: str | None = None

    booking_status: str | None = None


class BookingResponse(BaseModel):

    id: int

    booking_reference: str

    passenger_id: int

    flight_id: int

    journey_date: date

    seat_number: str

    booking_status: str

    checked_in: bool

    boarded: bool

    created_at: datetime

    model_config = {
        "from_attributes": True
    }