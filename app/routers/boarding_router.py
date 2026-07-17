from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.schemas.boarding_schema import BoardingRequest
from app.services.boarding_service import BoardingService
from app.utils.auth import get_current_user

router = APIRouter(
    prefix="",
    tags=["Boarding Management"]
)


@router.post("/checkin/{booking_id}")
def check_in(
    booking_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    return BoardingService.check_in(
        db=db,
        booking_id=booking_id,
        current_user=current_user
    )


@router.post("/boarding/{booking_id}")
def board_passenger(
    booking_id: int,
    request: BoardingRequest,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    return BoardingService.board_passenger(
        db=db,
        booking_id=booking_id,
        gate_number=request.gate_number,
        current_user=current_user
    )


@router.get("/passengers/{passenger_id}/bookings")
def passenger_history(
    passenger_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    return BoardingService.get_passenger_history(
        db=db,
        passenger_id=passenger_id,
        current_user=current_user
    )