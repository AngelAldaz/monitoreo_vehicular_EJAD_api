from fastapi import APIRouter, Depends, HTTPException, status, Body
from typing import List
import app.schemas.fuelStopSchema as fuelStopSchema
import app.services.fuelStopService as fuelStopService
import app.repositories.fuelStopRepository as fuelStopRepository
import app.repositories.vehicleRepository as vehicleRepository
import app.repositories.routeRepository as routeRepository
from app.database import get_db
from sqlalchemy.orm import Session


router = APIRouter(
    prefix="/fuel-stops",
    tags=["fuel-stops"],
    responses={404: {"description": "Not found"}},
)

def get_fuel_stop_service(db: Session = Depends(get_db)):
    repo = fuelStopRepository.FuelStopRepository(db)
    vehicle_repo = vehicleRepository.VehicleRepository(db)
    route_repo = routeRepository.RouteRepository(db)
    return fuelStopService.FuelStopService(repo, vehicle_repo, route_repo)

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

@router.post(
    "/start-refueling",
    response_model=fuelStopSchema.FuelStopStartResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Start a fuel stop and change vehicle status to REFUELING",
    response_description="The created fuel stop with vehicle status updated"
)
async def start_refueling(
    fuel_stop_data: fuelStopSchema.FuelStopStartSchema = Body(..., example={
        "id_route_fk": 1, 
        "latitude_stop": 12.345678, 
        "longitude_stop": 98.765432, 
        "stop_time": "2023-01-01T12:00:00Z"
    }),
    service: fuelStopService.FuelStopService = Depends(get_fuel_stop_service)
):
    """
    Inicia una parada para reabastecimiento de combustible con los siguientes detalles:
    - **id_route_fk**: ID de la ruta activa
    - **latitude_stop**: Latitud donde se detuvo el vehículo
    - **longitude_stop**: Longitud donde se detuvo el vehículo
    - **stop_time**: Hora en que se detuvo el vehículo
    
    Esta acción también cambiará el estado del vehículo a REFUELING.
    """
    return service.start_refueling(fuel_stop_data)

@router.post(
    "/finish-refueling",
    response_model=fuelStopSchema.FuelStopFinishResponse,
    status_code=status.HTTP_200_OK,
    summary="Finish a fuel stop and change vehicle status back to ON_ROUTE",
    response_description="The updated fuel stop with vehicle status changed back to ON_ROUTE",
    responses={
        status.HTTP_404_NOT_FOUND: {"description": "Fuel stop not found"},
        status.HTTP_400_BAD_REQUEST: {"description": "Vehicle is not in REFUELING state"}
    }
)
async def finish_refueling(
    fuel_stop_data: fuelStopSchema.FuelStopFinishSchema = Body(..., example={
        "id_fuel_stop": 1,
        "resume_time": "2023-01-01T12:30:00Z",
        "start_time": "2023-01-01T12:35:00Z",
        "latitude_start": 12.345679,
        "longitude_start": 98.765433,
        "liters_added": 45.5,
        "current_km": 10250,
        "image_km": "path/to/odometer_image.jpg"
    }),
    service: fuelStopService.FuelStopService = Depends(get_fuel_stop_service)
):
    """
    Finaliza una parada de reabastecimiento de combustible con los siguientes detalles:
    - **id_fuel_stop**: ID de la parada de combustible a finalizar
    - **resume_time**: Hora en que se terminó de cargar combustible
    - **start_time**: Hora en que el vehículo continuó su ruta
    - **latitude_start**: Latitud desde donde se reanudó la ruta
    - **longitude_start**: Longitud desde donde se reanudó la ruta
    - **liters_added**: Cantidad de litros de combustible agregados
    - **current_km**: Lectura actual del odómetro del vehículo
    - **image_km**: Ruta a la imagen del odómetro
    
    Esta acción también cambiará el estado del vehículo de vuelta a ON_ROUTE.
    """
    return service.finish_refueling(fuel_stop_data)








