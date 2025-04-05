from pydantic import BaseModel, Field
from datetime import datetime, time
from typing import Optional
# from enum import Enum
from enum import Enum as PyEnum

# class MaintenanceStatus(str, Enum):
#   IN_PROGRESS = "In Progress"
#   COMPLETED = "Completed"
#   CANCELLED = "Cancelled"
class MaintenanceStatus(str, PyEnum):
  IN_PROGRESS = "In Progress"
  COMPLETED = "Completed"
  CANCELLED = "Cancelled"

class MaintenanceBase(BaseModel):
  # id_vehicle_fk: int
  description: Optional[str] = None
  start_time: datetime
  estimated_time: time
  end_time: Optional[datetime] = None
  status: MaintenanceStatus

class MaintenanceCreate(MaintenanceBase):
  pass

class MaintenanceOut(MaintenanceBase):
  id_maintenance: int

  class Config:
    from_attributes = True

class MaintenanceUpdate(BaseModel):
  description: Optional[str] = None
  estimated_time: Optional[time] = None
  end_time: Optional[datetime] = None
  status: Optional[MaintenanceStatus] = None