from enum import Enum as PyEnum

class VehicleAssignmentStatus(str, PyEnum):
    ASSIGNED = "Assigned"
    NOT_ASSIGNED = "Not Assigned"
