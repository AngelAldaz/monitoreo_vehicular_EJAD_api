from fastapi import APIRouter, Depends, HTTPException, status, Body
from typing import List
import app.schemas.routesSchema as routesSchema
import app.schemas.fuelStopSchema as fuelStopSchema
import app.services.routeService as routeService
import app.services.fuelStopService as fuelStopService
import app.repositories.routeRepository as routeRepository
import app.repositories.vehicleRepository as vehicleRepository
import app.repositories.fuelStopRepository as fuelStopRepository
from app.database import get_db
from sqlalchemy.orm import Session

router = APIRouter(
    prefix="/routes",
    tags=["routes"],
    responses={404: {"description": "Not found"}}
)

def get_route_service(db: Session = Depends(get_db)):
    repo = routeRepository.RouteRepository(db)
    vehicle_repo = vehicleRepository.VehicleRepository(db)
    return routeService.RouteService(repo, vehicle_repo)

def get_fuel_stop_service(db: Session = Depends(get_db)):
    repo = fuelStopRepository.FuelStopRepository(db)
    vehicle_repo = vehicleRepository.VehicleRepository(db)
    route_repo = routeRepository.RouteRepository(db)
    return fuelStopService.FuelStopService(repo, vehicle_repo, route_repo)

@router.post(
    "/",
    response_model=routesSchema.RouteOut,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new route",
    response_description="The created route"
)
async def create_route(
    route_data: routesSchema.RouteCreate = Body(..., example={"id_vehicle_fk": 1, "id_user_fk": 1, "description": "Route description", "latitude_start": 12.345678, "longitude_start": 98.765432, "latitude_end": 12.345678, "longitude_end": 98.765432, "start_time": "2021-01-01T00:00:00Z", "end_time": "2021-01-01T00:00:00Z", "estimated_time": 100, "total_duration": 100, "on_time": 100, "start_km": 100, "end_km": 100, "estimated_km": 100, "image_start_km": "image_start_km", "image_end_km": "image_end_km", "on_distance": 100, "liters_consumed": 100}),
    service: routeService.RouteService = Depends(get_route_service)
):
    return service.create_route(route_data)

@router.get(
    "/{route_id}",
    response_model=routesSchema.RouteOut,
    summary="Get a route by ID",
    responses={404: {"description": "Route not found"}}
)
async def get_route(
    route_id: int,
    service: routeService.RouteService = Depends(get_route_service)
):
    route = service.get_route_by_id(route_id)
    if not route:
        raise HTTPException(status_code=404, detail="Route not found")
    return route

@router.get(
    "/",
    response_model=List[routesSchema.RouteOut],
    summary="Get all routes"
)
async def list_routes(
    service: routeService.RouteService = Depends(get_route_service)
):
    return service.get_all_routes()

@router.put(
    "/{route_id}",
    response_model=routesSchema.RouteOut,
    summary="Update a route",
    responses={
        200: {"description": "Route updated successfully"},
        404: {"description": "Route not found"}
    }
)   
async def update_route(
    route_id: int,
    route_data: routesSchema.RouteCreate = Body(..., example={"id_vehicle_fk": 1, "id_user_fk": 1, "description": "Route description", "latitude_start": 12.345678, "longitude_start": 98.765432, "latitude_end": 12.345678, "longitude_end": 98.765432, "start_time": "2021-01-01T00:00:00Z", "end_time": "2021-01-01T00:00:00Z", "estimated_time": 100, "total_duration": 100, "on_time": 100, "start_km": 100, "end_km": 100, "estimated_km": 100, "image_start_km": "image_start_km", "image_end_km": "image_end_km", "on_distance": 100, "liters_consumed": 100}),
    service: routeService.RouteService = Depends(get_route_service)
):
    return service.update_route(route_id, route_data)

@router.delete(
    "/{route_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a route",
    responses={
        204: {"description": "Route deleted successfully"},
        404: {"description": "Route not found"}
    }
)
async def delete_route(
    route_id: int,
    service: routeService.RouteService = Depends(get_route_service)
):
    if not service.delete_route(route_id):
        raise HTTPException(status_code=404, detail="Route not found")
    return None

@router.post(
    "/start",
    response_model=routesSchema.RouteStartResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Start a new route",
    response_description="The started route"
)
async def start_route(
    route_data: routesSchema.RouteStartSchema = Body(..., example={
        "id_vehicle_fk": 1, 
        "id_user_fk": 1, 
        "latitude_start": 12.345678, 
        "longitude_start": 98.765432, 
        "start_time": "2023-01-01T08:00:00Z", 
        "start_km": 10000, 
        "image_start_km": "path/to/image.jpg",
        "description": "Route in progress"
    }),
    service: routeService.RouteService = Depends(get_route_service)
):
    """
    Start a new route with the following details:
    - **id_vehicle_fk**: ID of the vehicle
    - **id_user_fk**: ID of the user (driver)
    - **latitude_start**: Starting latitude
    - **longitude_start**: Starting longitude
    - **start_time**: Time when the route starts
    - **start_km**: Current vehicle odometer reading
    - **image_start_km**: Path to the image of the odometer
    - **description**: Optional description (defaults to "Route in progress")
    
    This will also change the vehicle's status to ON_ROUTE.
    """
    return service.start_route(route_data)

@router.post(
    "/finish",
    response_model=routesSchema.RouteEndResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Finish a route",
    response_description="The finished route"
)
async def finish_route(
    route_data: routesSchema.RouteEndSchema = Body(..., example={
        "id_vehicle_fk": 1, 
        "id_user_fk": 1, 
        "latitude_end": 12.345678, 
        "longitude_end": 98.765432, 
        "end_time": "2023-01-01T08:00:00Z", 
        "end_km": 10000, 
        "image_end_km": "path/to/image.jpg"
    }),
    service: routeService.RouteService = Depends(get_route_service)
):
    """
    Finish a route with the following details:
    - **id_vehicle_fk**: ID of the vehicle
    - **id_user_fk**: ID of the user (driver)
    - **latitude_end**: Ending latitude
    - **longitude_end**: Ending longitude
    - **end_time**: Time when the route ends
    - **end_km**: Current vehicle odometer reading
    - **image_end_km**: Path to the image of the odometer
    """
    return service.end_route(route_data)

@router.get(
    "/{route_id}/fuel-stops",
    response_model=List[fuelStopSchema.FuelStopOut],
    summary="Get all fuel stops for a specific route",
    responses={
        200: {"description": "List of fuel stops for the route"},
        404: {"description": "Route not found"}
    }
)
async def get_route_fuel_stops(
    route_id: int,
    route_service: routeService.RouteService = Depends(get_route_service),
    fuel_stop_service: fuelStopService.FuelStopService = Depends(get_fuel_stop_service)
):
    """
    Retrieve all fuel stops associated with a specific route.
    
    This endpoint returns a list of all fuel stops that occurred during a route,
    including details such as stop times, fuel amounts, and locations.
    """
    route = route_service.get_route_by_id(route_id)
    if not route:
        raise HTTPException(status_code=404, detail="Route not found")
    
    # Get all fuel stops for this route using the service
    return fuel_stop_service.get_fuel_stops_by_route_id(route_id)