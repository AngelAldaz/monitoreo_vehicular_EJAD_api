from fastapi import APIRouter, Depends, HTTPException, status, Body
from typing import List
import app.schemas.vehiclesSchema as vehiclesSchema
import app.schemas.routesSchema as routesSchema
import app.services.vehicleService as vehicleService
import app.repositories.vehicleRepository as vehicleRepository
import app.repositories.routeRepository as routeRepository
from app.database import get_db
from sqlalchemy.orm import Session
from fastapi.responses import StreamingResponse

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
    vehicle_data: vehiclesSchema.VehicleUpdate = Body(..., example={"number_plate": "ABC123", "serial_number": "1234567890", "year": 2020, "color": "Red", "km": 10000, "km_per_litre": 10, "id_model_fk": 1, "id_description_fk": 1, "id_brand_fk": 1}),
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

@router.get(
    "/{vehicle_id}/export-excel",
    summary="Export vehicle data to Excel",
    responses={
        200: {"description": "Excel file with vehicle data", "content": {"application/vnd.openxmlformats-officedocument.spreadsheetml.sheet": {}}},
        404: {"description": "Vehicle not found"}
    }
)
async def export_vehicle_to_excel(
    vehicle_id: int,
    service: vehicleService.VehicleService = Depends(get_vehicle_service)
):
    """
    Export vehicle data to Excel with all its routes and fuel stops.
    
    This endpoint generates an Excel report containing:
    - Vehicle information
    - List of all routes for the vehicle
    - Details of fuel stops for each route
    
    The Excel file will contain multiple sheets, including:
    - Vehicle details
    - Routes summary
    - Fuel stops for each route (as separate sheets)
    """
    try:
        excel_file = service.generate_vehicle_excel_report(vehicle_id)
        
        # Return the Excel file as a response
        return StreamingResponse(
            excel_file,
            media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            headers={"Content-Disposition": f"attachment; filename=vehicle_{vehicle_id}_report.xlsx"}
        )
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating Excel file: {str(e)}")

@router.get(
    "/{vehicle_id}/routes",
    response_model=List[routesSchema.RouteOut],
    summary="Get all routes for a specific vehicle",
    responses={
        200: {"description": "List of routes for the vehicle"},
        404: {"description": "Vehicle not found"}
    }
)
async def get_vehicle_routes(
    vehicle_id: int,
    service: vehicleService.VehicleService = Depends(get_vehicle_service)
):
    """
    Retrieve all routes associated with a specific vehicle.
    
    This endpoint returns a list of all routes that have been assigned to the vehicle,
    including details such as start/end times, locations, and distances.
    """
    vehicle = service.get_vehicle_by_id(vehicle_id)
    if not vehicle:
        raise HTTPException(status_code=404, detail="Vehicle not found")
    
    # Get all routes for this vehicle using the service method
    return service.get_vehicle_routes(vehicle_id)

