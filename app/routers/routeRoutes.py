from fastapi import APIRouter, Depends, HTTPException, status, Body
from typing import List
import app.schemas.routesSchema as routesSchema
import app.services.routeService as routeService
import app.repositories.routeRepository as routeRepository
from app.database import get_db
from sqlalchemy.orm import Session

router = APIRouter(
    prefix="/routes",
    tags=["routes"],
    responses={404: {"description": "Not found"}}
)

def get_route_service(db: Session = Depends(get_db)):
    repo = routeRepository.RouteRepository(db)
    return routeService.RouteService(repo)


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
