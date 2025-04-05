from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class FuelStopBase(BaseModel):
    id_route_fk: int
    latitude_stop: float
    longitude_stop: float
    stop_time: datetime
    resume_time: Optional[datetime] = None
    start_time: Optional[datetime] = None
    latitude_start: Optional[float] = None
    longitude_start: Optional[float] = None
    liters_added: float

class FuelStopCreate(FuelStopBase):
    pass

class FuelStopUpdate(FuelStopBase):
    pass

class FuelStopOut(FuelStopBase):
    id_fuel_stop: int
    route_name: Optional[str] = None

    class Config:
        from_attributes = True

    
    
