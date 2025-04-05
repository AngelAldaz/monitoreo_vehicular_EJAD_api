from pydantic import BaseModel
from typing import Optional, Union
from datetime import datetime


class RouteBase(BaseModel):
    id_vehicle_fk: int
    id_user_fk: int
    description: str
    latitude_start: Union[str, float]
    longitude_start: Union[str, float]
    latitude_end: Union[str, float]
    longitude_end: Union[str, float]
    start_time: datetime
    end_time: datetime
    estimated_time: float
    total_duration: float
    on_time: Union[bool, int]
    start_km: int
    end_km: int
    estimated_km: int
    image_start_km: str
    image_end_km: str
    on_distance: Union[bool, int]
    liters_consumed: float

class RouteCreate(RouteBase):
    pass

class RouteUpdate(RouteBase):
    pass

class RouteOut(RouteBase):
    id_route: int
    name_vehicle: Optional[str] = None
    name_user: Optional[str] = None

    class Config:
        from_attributes = True

class RouteStartSchema(BaseModel):
    id_vehicle_fk: int
    id_user_fk: int
    latitude_start: Union[str, float]
    longitude_start: Union[str, float]
    start_time: datetime
    start_km: int
    image_start_km: str
    description: str = "Route in progress"
    
class RouteEndSchema(BaseModel):
    id_route: int
    id_vehicle_fk: int
    id_user_fk: int
    latitude_end: Union[str, float]
    longitude_end: Union[str, float]
    end_time: datetime
    end_km: int
    image_end_km: str
    description: str = "Route in progress"
    
class RouteStartResponse(BaseModel):
    id_route: int
    id_vehicle_fk: int
    id_user_fk: int
    description: str
    latitude_start: str
    longitude_start: str
    start_time: datetime
    start_km: int
    image_start_km: str
    name_vehicle: Optional[str] = None
    name_user: Optional[str] = None
    
    class Config:
        from_attributes = True
        
class RouteEndResponse(RouteStartResponse):
    latitude_end: str
    longitude_end: str
    end_time: datetime
    end_km: int
    image_end_km: str
    route_status: str
    
    class Config:
        from_attributes = True
        

