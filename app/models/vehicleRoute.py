from enum import Enum as PyEnum

class vehicleRoute(str, PyEnum):
    ON_ROUTE = "On Route"
    OFF_ROUTE = "Off Route"
    REFUELING = "Refueling"
