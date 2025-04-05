from pydantic import BaseModel
from typing import Optional

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

class VehicleUpdate(VehicleBase):
    pass

class VehicleOut(VehicleBase):
    id_vehicle: int
    name_model: Optional[str] = None
    name_description: Optional[str] = None
    name_brand: Optional[str] = None

    class Config:
        from_attributes = True
    
