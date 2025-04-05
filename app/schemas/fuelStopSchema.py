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

class FuelStopStartSchema(BaseModel):
    id_route_fk: int
    latitude_stop: float
    longitude_stop: float
    stop_time: datetime
    
class FuelStopStartResponse(BaseModel):
    id_fuel_stop: int
    id_route_fk: int
    latitude_stop: float
    longitude_stop: float
    stop_time: datetime
    route_name: Optional[str] = None
    vehicle_status: str
    
    class Config:
        from_attributes = True

class FuelStopFinishSchema(BaseModel):
    id_fuel_stop: int
    resume_time: datetime
    start_time: datetime
    latitude_start: float
    longitude_start: float
    liters_added: float
    current_km: int
    image_km: str
    
class FuelStopFinishResponse(BaseModel):
    id_fuel_stop: int
    id_route_fk: int
    latitude_stop: float
    longitude_stop: float
    stop_time: datetime
    resume_time: datetime
    start_time: datetime
    latitude_start: float
    longitude_start: float
    liters_added: float
    current_km: int
    image_km: str
    route_name: Optional[str] = None
    vehicle_status: str
    
    class Config:
        from_attributes = True

    
    
