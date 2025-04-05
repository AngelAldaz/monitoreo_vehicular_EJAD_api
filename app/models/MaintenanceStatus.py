# import enum
from enum import Enum as PyEnum


# class MaintenanceStatus(enum.Enum):
#     IN_PROGRESS = "In Progress"
#     COMPLETED = "Completed"
#     CANCELLED = "Cancelled"

class MaintenanceStatus(str, PyEnum):
  IN_PROGRESS = "In Progress"
  COMPLETED = "Completed"
  CANCELLED = "Cancelled"
