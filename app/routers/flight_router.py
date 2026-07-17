from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.dependencies import admin_only, admin_or_passenger
from app.schemas.flight_schema import (
    FlightCreate,
    FlightUpdate
)
from app.services.flight_service import FlightService

router = APIRouter(
    prefix="/flights",
    tags=["Flight Management"]
)


@router.post(
    "",
    status_code=status.HTTP_201_CREATED
)
def create_flight(
    request: FlightCreate,
    db: Session = Depends(get_db),
    current_user=Depends(admin_only)
):
    return FlightService.create_flight(db, request)


@router.get("")
def get_all_flights(
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user=Depends(admin_or_passenger)
):
    return FlightService.get_all_flights(
        db,
        page,
        limit
    )


@router.get("/{flight_id}")
def get_flight(
    flight_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(admin_or_passenger)
):
    return FlightService.get_flight_by_id(
        db,
        flight_id
    )


@router.put("/{flight_id}")
def update_flight(
    flight_id: int,
    request: FlightUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(admin_only)
):
    return FlightService.update_flight(
        db,
        flight_id,
        request
    )


@router.delete("/{flight_id}")
def delete_flight(
    flight_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(admin_only)
):
    return FlightService.delete_flight(
        db,
        flight_id
    )