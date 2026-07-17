from fastapi import FastAPI

from app.database.database import Base
from app.database.database import engine

from app.exceptions.handlers import register_exception_handlers

from app.routers.auth_router import router as auth_router
from app.routers.flight_router import router as flight_router
from app.routers.booking_router import router as booking_router
from app.routers.boarding_router import router as boarding_router
from app.routers.report_router import router as report_router

app = FastAPI(
    title="Airline Reservation & Flight Management System",
    version="1.0.0"
)

Base.metadata.create_all(bind=engine)

register_exception_handlers(app)

app.include_router(auth_router)
app.include_router(flight_router)
app.include_router(booking_router)
app.include_router(boarding_router)
app.include_router(report_router)


@app.get("/")
def home():
    return {
        "message": "Airline Reservation API Running Successfully"
    }