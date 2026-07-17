from fastapi import APIRouter
from fastapi import Depends
from fastapi import Query
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.dependencies import admin_only, admin_or_passenger
from app.services.report_service import ReportService

router = APIRouter(
    prefix="/reports",
    tags=["Reports"]
)


@router.get("/flights/search")
def search_flights(
    source: str | None = None,
    destination: str | None = None,
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1),
    db: Session = Depends(get_db),
    current_user=Depends(admin_or_passenger)
):

    return ReportService.search_flights(
        db=db,
        source=source,
        destination=destination,
        page=page,
        limit=limit
    )


@router.get("/bookings/status")
def booking_status(
    status: str,
    page: int = Query(1),
    limit: int = Query(10),
    db: Session = Depends(get_db),
    current_user=Depends(admin_only)
):

    return ReportService.bookings_by_status(
        db=db,
        status=status,
        page=page,
        limit=limit
    )


@router.get("/passenger-history/{passenger_id}")
def passenger_history(
    passenger_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(admin_or_passenger)
):

    if (
        current_user.role == "Passenger"
        and current_user.id != passenger_id
    ):
        from fastapi import HTTPException

        raise HTTPException(
            status_code=403,
            detail="Permission Denied"
        )

    return ReportService.passenger_history(
        db=db,
        passenger_id=passenger_id
    )


@router.get("/dashboard")
def dashboard(
    db: Session = Depends(get_db),
    current_user=Depends(admin_only)
):

    return ReportService.dashboard(db)


@router.get("/flight-statistics")
def statistics(
    db: Session = Depends(get_db),
    current_user=Depends(admin_only)
):

    return ReportService.flight_statistics(db)