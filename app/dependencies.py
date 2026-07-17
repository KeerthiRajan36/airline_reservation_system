from app.utils.role_checker import RoleChecker


admin_only = RoleChecker(
    ["Admin"]
)

passenger_only = RoleChecker(
    ["Passenger"]
)

admin_or_passenger = RoleChecker(
    [
        "Admin",
        "Passenger"
    ]
)