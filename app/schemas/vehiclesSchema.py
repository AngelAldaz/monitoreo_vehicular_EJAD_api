from pydantic import BaseModel
from sqlalchemy import Column, Integer, String, ForeignKey, Enum
from typing import Optional
from app.models.vehicleRoute import vehicleRoute
from app.models.VehicleAssignmentStatus import VehicleAssignmentStatus

class VehicleBase(BaseModel):
    number_plate: str
    serial_number: str
    year: int
    color: str
    km: int
    km_per_litre: int
    id_model_fk: int
    id_description_fk: int
    id_brand_fk: int

class VehicleCreate(VehicleBase):   
    pass

# class VehicleUpdate(VehicleBase):
#     pass

class VehicleOut(VehicleBase):
    id_vehicle: int
    name_model: Optional[str] = None
    name_description: Optional[str] = None
    name_brand: Optional[str] = None

    class Config:
        from_attributes = True
    
class VehicleUpdate(BaseModel):
  number_plate: Optional[str] = None
  year: Optional[int] = None
  color: Optional[str] = None
  km: Optional[int] = None
  route_status: Optional[vehicleRoute] = None
  assignment_status: Optional[VehicleAssignmentStatus] = None