class AirlineException(Exception):
    """Base Exception"""
    pass


class UserAlreadyExistsException(AirlineException):
    pass


class InvalidCredentialsException(AirlineException):
    pass


class UnauthorizedException(AirlineException):
    pass


class ForbiddenException(AirlineException):
    pass


class FlightNotFoundException(AirlineException):
    pass


class FlightAlreadyExistsException(AirlineException):
    pass


class BookingNotFoundException(AirlineException):
    pass


class SeatAlreadyBookedException(AirlineException):
    pass


class JourneyDateException(AirlineException):
    pass


class FlightCapacityException(AirlineException):
    pass


class BookingCancelledException(AirlineException):
    pass


class CheckInNotAllowedException(AirlineException):
    pass


class BoardingNotAllowedException(AirlineException):
    pass


class BoardingAlreadyCompletedException(AirlineException):
    pass


class PassengerNotFoundException(AirlineException):
    pass


class InvalidStatusException(AirlineException):
    pass