from datetime import datetime

from pydantic import BaseModel


class BoardingRequest(BaseModel):

    gate_number: str


class BoardingResponse(BaseModel):

    id: int

    booking_id: int

    gate_number: str | None

    boarding_time: datetime | None

    boarding_status: str

    model_config = {
        "from_attributes": True
    }