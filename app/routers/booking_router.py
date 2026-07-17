from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.dependencies import admin_or_passenger
from app.schemas.booking_schema import (
    BookingCreate,
    BookingUpdate
)
from app.services.booking_service import BookingService
from app.utils.auth import get_current_user

router = APIRouter(
    prefix="/bookings",
    tags=["Booking Management"]
)


@router.post("")
def create_booking(
    request: BookingCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    return BookingService.create_booking(
        db,
        current_user,
        request
    )


@router.get("")
def get_all_bookings(
    page: int = Query(1, ge=1),
    limit: int = Query(10, le=100),
    db: Session = Depends(get_db),
    current_user=Depends(admin_or_passenger)
):
    return BookingService.get_all_bookings(
        db,
        page,
        limit
    )


@router.get("/{booking_id}")
def get_booking(
    booking_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    booking = BookingService.get_booking_by_id(
        db,
        booking_id
    )

    if (
        current_user.role == "Passenger"
        and booking.passenger_id != current_user.id
    ):
        from fastapi import HTTPException
        raise HTTPException(
            status_code=403,
            detail="Permission Denied"
        )

    return booking


@router.put("/{booking_id}")
def update_booking(
    booking_id: int,
    request: BookingUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    booking = BookingService.get_booking_by_id(
        db,
        booking_id
    )

    if (
        current_user.role == "Passenger"
        and booking.passenger_id != current_user.id
    ):
        from fastapi import HTTPException
        raise HTTPException(
            status_code=403,
            detail="Permission Denied"
        )

    return BookingService.update_booking(
        db,
        booking_id,
        request
    )

