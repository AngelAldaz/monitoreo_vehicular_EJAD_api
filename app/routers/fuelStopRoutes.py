from fastapi import APIRouter, Depends, HTTPException, status, Body
from typing import List
import app.schemas.fuelStopSchema as fuelStopSchema
import app.services.fuelStopService as fuelStopService
import app.repositories.fuelStopRepository as fuelStopRepository
from app.database import get_db
from sqlalchemy.orm import Session


router = APIRouter(
    prefix="/fuel-stops",
    tags=["fuel-stops"],
    responses={404: {"description": "Not found"}},
)

def get_fuel_stop_service(db: Session = Depends(get_db)):
    repo = fuelStopRepository.FuelStopRepository(db)
    return fuelStopService.FuelStopService(repo)

@router.post(
    "/",
    response_model=fuelStopSchema.FuelStopOut,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new fuel stop",
    response_description="The created fuel stop"
)   
async def create_fuel_stop(
    fuel_stop_data: fuelStopSchema.FuelStopCreate = Body(..., example={"id_route_fk": 1, "latitude_stop": 12.3456, "longitude_stop": 78.9101, "stop_time": "2023-01-01T12:00:00Z", "resume_time": "2023-01-01T12:00:00Z", "start_time": "2023-01-01T12:00:00Z", "latitude_start": 12.3456, "longitude_start": 78.9101, "liters_added": 10.0}),
    service: fuelStopService.FuelStopService = Depends(get_fuel_stop_service)
):
    return service.create_fuel_stop(fuel_stop_data)

@router.get(
    "/{fuel_stop_id}",
    response_model=fuelStopSchema.FuelStopOut,
    summary="Get a fuel stop by ID",
    responses={404: {"description": "Fuel stop not found"}}
)
async def get_fuel_stop(
    fuel_stop_id: int,
    service: fuelStopService.FuelStopService = Depends(get_fuel_stop_service)
):
    fuel_stop = service.get_fuel_stop_by_id(fuel_stop_id)
    if not fuel_stop:
        raise HTTPException(status_code=404, detail="Fuel stop not found")
    return fuel_stop

@router.get(
    "/",
    response_model=List[fuelStopSchema.FuelStopOut],
    summary="Get all fuel stops"
)
async def list_fuel_stops(
    service: fuelStopService.FuelStopService = Depends(get_fuel_stop_service)
):
    return service.get_all_fuel_stops()

@router.put(
    "/{fuel_stop_id}",
    response_model=fuelStopSchema.FuelStopOut,
    summary="Update a fuel stop",
    responses={
        status.HTTP_200_OK: {"description": "Fuel stop updated successfully"},
        404: {"description": "Fuel stop not found"}
    }
)
async def update_fuel_stop(
    fuel_stop_id: int,
    fuel_stop_data: fuelStopSchema.FuelStopCreate = Body(..., example={"id_route_fk": 1, "latitude_stop": 12.3456, "longitude_stop": 78.9101, "stop_time": "2023-01-01T12:00:00Z", "resume_time": "2023-01-01T12:00:00Z", "start_time": "2023-01-01T12:00:00Z", "latitude_start": 12.3456, "longitude_start": 78.9101, "liters_added": 10.0}),
    service: fuelStopService.FuelStopService = Depends(get_fuel_stop_service)
):
    updated_fuel_stop = service.update_fuel_stop(fuel_stop_id, fuel_stop_data)
    if not updated_fuel_stop:
        raise HTTPException(status_code=404, detail="Fuel stop not found")
    return updated_fuel_stop

@router.delete(
    "/{fuel_stop_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a fuel stop",
    responses={
        status.HTTP_204_NO_CONTENT: {"description": "Fuel stop deleted successfully"},
        404: {"description": "Fuel stop not found"}
    }
)
async def delete_fuel_stop(
    fuel_stop_id: int,
    service: fuelStopService.FuelStopService = Depends(get_fuel_stop_service)
):
    if not service.delete_fuel_stop(fuel_stop_id):
        raise HTTPException(status_code=404, detail="Fuel stop not found")
    return None








