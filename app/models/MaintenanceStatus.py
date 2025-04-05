import enum

class MaintenanceStatus(enum.Enum):
    IN_PROGRESS = "In Progress"
    COMPLETED = "Completed"
    CANCELLED = "Cancelled"
