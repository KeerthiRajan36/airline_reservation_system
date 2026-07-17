from datetime import datetime

from pydantic import BaseModel
from pydantic import Field


class FlightCreate(BaseModel):

    flight_number: str = Field(..., example="AI101")

    airline_name: str = Field(..., example="Air India")

    source: str = Field(..., example="Chennai")

    destination: str = Field(..., example="Delhi")

    departure_time: datetime

    arrival_time: datetime

    total_seats: int = Field(..., gt=0)


class FlightUpdate(BaseModel):

    airline_name: str | None = None

    source: str | None = None

    destination: str | None = None

    departure_time: datetime | None = None

    arrival_time: datetime | None = None

    total_seats: int | None = None

    status: str | None = None


class FlightResponse(BaseModel):

    id: int
    flight_number: str
    airline_name: str
    source: str
    destination: str
    departure_time: datetime
    arrival_time: datetime
    total_seats: int
    available_seats: int
    status: str

    model_config = {
        "from_attributes": True
    }