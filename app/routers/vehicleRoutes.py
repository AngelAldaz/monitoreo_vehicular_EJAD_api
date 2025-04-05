from fastapi import APIRouter, Depends, HTTPException, status, Body
from typing import List
import app.schemas.vehiclesSchema as vehiclesSchema
import app.services.vehicleService as vehicleService
import app.repositories.vehicleRepository as vehicleRepository
from app.database import get_db
from sqlalchemy.orm import Session

router = APIRouter(
  prefix="/vehicles",
  tags=["vehicles"],
  responses={404: {"description": "Not found"}},
)

def get_vehicle_service(db: Session = Depends(get_db)):
    repo = vehicleRepository.VehicleRepository(db)
    return vehicleService.VehicleService(repo)

@router.post(
    "/",
    response_model=vehiclesSchema.VehicleOut,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new vehicle",
    response_description="The created vehicle"
)
async def create_vehicle(
    vehicle_data: vehiclesSchema.VehicleCreate = Body(..., example={"number_plate": "ABC123", "serial_number": "1234567890", "year": 2020, "color": "Red", "km": 10000, "km_per_litre": 10, "id_model_fk": 1, "id_description_fk": 1, "id_brand_fk": 1}),
    service: vehicleService.VehicleService = Depends(get_vehicle_service)
):
    return service.create_vehicle(vehicle_data)

@router.get(
    "/{vehicle_id}",
    response_model=vehiclesSchema.VehicleOut,
    summary="Get a vehicle by ID",
    responses={404: {"description": "Vehicle not found"}}
)
async def get_vehicle(
    vehicle_id: int,
    service: vehicleService.VehicleService = Depends(get_vehicle_service)
):
    vehicle = service.get_vehicle_by_id(vehicle_id)
    if not vehicle:
        raise HTTPException(status_code=404, detail="Vehicle not found")
    return vehicle

@router.get(
    "/",
    response_model=List[vehiclesSchema.VehicleOut],
    summary="Get all vehicles"
)
async def list_vehicles(
    service: vehicleService.VehicleService = Depends(get_vehicle_service)
):
    return service.get_all_vehicles()

@router.put(
    "/{vehicle_id}",
    response_model=vehiclesSchema.VehicleOut,
    summary="Update a vehicle",
    responses={
        200: {"description": "Vehicle updated successfully"},
        404: {"description": "Vehicle not found"}
    }
)
async def update_vehicle(
    vehicle_id: int,
    vehicle_data: vehiclesSchema.VehicleCreate = Body(..., example={"number_plate": "ABC123", "serial_number": "1234567890", "year": 2020, "color": "Red", "km": 10000, "km_per_litre": 10, "id_model_fk": 1, "id_description_fk": 1, "id_brand_fk": 1}),
    service: vehicleService.VehicleService = Depends(get_vehicle_service)
):
    updated_vehicle = service.update_vehicle(vehicle_id, vehicle_data)
    if not updated_vehicle:
        raise HTTPException(status_code=404, detail="Vehicle not found")    
    return updated_vehicle

@router.delete(
    "/{vehicle_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a vehicle",   
    responses={
        204: {"description": "Vehicle deleted successfully"},
        404: {"description": "Vehicle not found"}
    }
)
async def delete_vehicle(
    vehicle_id: int,
    service: vehicleService.VehicleService = Depends(get_vehicle_service)
):
    success = service.delete_vehicle(vehicle_id)
    if not success:
        raise HTTPException(status_code=404, detail="Vehicle not found")
    return None

