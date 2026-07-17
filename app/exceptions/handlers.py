from fastapi import FastAPI
from fastapi import Request
from fastapi.responses import JSONResponse

from app.exceptions.custom_exceptions import *


def register_exception_handlers(app: FastAPI):

    @app.exception_handler(UserAlreadyExistsException)
    async def user_exists(
        request: Request,
        exc: UserAlreadyExistsException
    ):
        return JSONResponse(
            status_code=409,
            content={
                "success": False,
                "message": "User already exists."
            }
        )

    @app.exception_handler(InvalidCredentialsException)
    async def invalid_credentials(
        request: Request,
        exc: InvalidCredentialsException
    ):
        return JSONResponse(
            status_code=401,
            content={
                "success": False,
                "message": "Invalid email or password."
            }
        )

    @app.exception_handler(UnauthorizedException)
    async def unauthorized(
        request: Request,
        exc: UnauthorizedException
    ):
        return JSONResponse(
            status_code=401,
            content={
                "success": False,
                "message": "Unauthorized access."
            }
        )

    @app.exception_handler(ForbiddenException)
    async def forbidden(
        request: Request,
        exc: ForbiddenException
    ):
        return JSONResponse(
            status_code=403,
            content={
                "success": False,
                "message": "Permission denied."
            }
        )

    @app.exception_handler(FlightAlreadyExistsException)
    async def duplicate_flight(
        request: Request,
        exc: FlightAlreadyExistsException
    ):
        return JSONResponse(
            status_code=409,
            content={
                "success": False,
                "message": "Flight number already exists."
            }
        )

    @app.exception_handler(FlightNotFoundException)
    async def flight_not_found(
        request: Request,
        exc: FlightNotFoundException
    ):
        return JSONResponse(
            status_code=404,
            content={
                "success": False,
                "message": "Flight not found."
            }
        )

    @app.exception_handler(BookingNotFoundException)
    async def booking_not_found(
        request: Request,
        exc: BookingNotFoundException
    ):
        return JSONResponse(
            status_code=404,
            content={
                "success": False,
                "message": "Booking not found."
            }
        )

    @app.exception_handler(SeatAlreadyBookedException)
    async def seat_booked(
        request: Request,
        exc: SeatAlreadyBookedException
    ):
        return JSONResponse(
            status_code=409,
            content={
                "success": False,
                "message": "Seat already booked."
            }
        )

    @app.exception_handler(FlightCapacityException)
    async def capacity_full(
        request: Request,
        exc: FlightCapacityException
    ):
        return JSONResponse(
            status_code=400,
            content={
                "success": False,
                "message": "No seats available."
            }
        )

    @app.exception_handler(JourneyDateException)
    async def journey_error(
        request: Request,
        exc: JourneyDateException
    ):
        return JSONResponse(
            status_code=400,
            content={
                "success": False,
                "message": "Journey date cannot be in the past."
            }
        )

    @app.exception_handler(CheckInNotAllowedException)
    async def checkin_error(
        request: Request,
        exc: CheckInNotAllowedException
    ):
        return JSONResponse(
            status_code=400,
            content={
                "success": False,
                "message": "Check-in is allowed only within 24 hours before departure."
            }
        )

    @app.exception_handler(BoardingNotAllowedException)
    async def boarding_error(
        request: Request,
        exc: BoardingNotAllowedException
    ):
        return JSONResponse(
            status_code=400,
            content={
                "success": False,
                "message": "Passenger must complete check-in before boarding."
            }
        )

    @app.exception_handler(BoardingAlreadyCompletedException)
    async def boarding_completed(
        request: Request,
        exc: BoardingAlreadyCompletedException
    ):
        return JSONResponse(
            status_code=400,
            content={
                "success": False,
                "message": "Passenger has already boarded."
            }
        )

    @app.exception_handler(BookingCancelledException)
    async def cancelled_booking(
        request: Request,
        exc: BookingCancelledException
    ):
        return JSONResponse(
            status_code=400,
            content={
                "success": False,
                "message": "Booking has been cancelled."
            }
        )

    @app.exception_handler(PassengerNotFoundException)
    async def passenger_not_found(
        request: Request,
        exc: PassengerNotFoundException
    ):
        return JSONResponse(
            status_code=404,
            content={
                "success": False,
                "message": "Passenger not found."
            }
        )

    @app.exception_handler(InvalidStatusException)
    async def invalid_status(
        request: Request,
        exc: InvalidStatusException
    ):
        return JSONResponse(
            status_code=400,
            content={
                "success": False,
                "message": "Invalid booking status."
            }
        )

    @app.exception_handler(Exception)
    async def global_exception(
        request: Request,
        exc: Exception
    ):
        return JSONResponse(
            status_code=500,
            content={
                "success": False,
                "message": str(exc)
            }
        )