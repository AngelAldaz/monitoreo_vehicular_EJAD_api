from typing import Optional
from app.schemas.vehiclesSchema import VehicleCreate, VehicleOut, VehicleUpdate
from app.repositories.vehicleRepository import VehicleRepository
from app.models.vehiclesModel import Vehicle
from app.utils.excelUtil import ExcelGenerator
from fastapi import HTTPException
from io import BytesIO
from app.schemas.routesSchema import RouteOut

class VehicleService:
  def __init__(self, vehicle_repo: VehicleRepository) -> None:
    self.repo = vehicle_repo

  def create_vehicle(self, vehicle: VehicleCreate) -> VehicleOut:
    db_vehicle = Vehicle(
      number_plate=vehicle.number_plate,
      serial_number=vehicle.serial_number,
      year=vehicle.year,
      color=vehicle.color,
      km=vehicle.km,
      km_per_litre=vehicle.km_per_litre,
      id_model_fk=vehicle.id_model_fk,
      id_description_fk=vehicle.id_description_fk,
      id_brand_fk=vehicle.id_brand_fk
    )
    created_vehicle = self.repo.create_vehicle(db_vehicle)
    return VehicleOut(
      id_vehicle=created_vehicle.id_vehicle,
      number_plate=created_vehicle.number_plate,
      serial_number=created_vehicle.serial_number,
      year=created_vehicle.year,
      color=created_vehicle.color,
      km=created_vehicle.km,
      km_per_litre=created_vehicle.km_per_litre,
      id_model_fk=created_vehicle.id_model_fk,
      id_description_fk=created_vehicle.id_description_fk,
      id_brand_fk=created_vehicle.id_brand_fk,
      name_model=created_vehicle.model.name if created_vehicle.model else None,
      name_description=created_vehicle.description.name if created_vehicle.description else None,
      name_brand=created_vehicle.brand.name if created_vehicle.brand else None
    )

  def get_vehicle_by_id(self, vehicle_id: int) -> Optional[VehicleOut]:
    db_vehicle = self.repo.get_vehicle_by_id(vehicle_id)
    if db_vehicle is not None:
      return VehicleOut(
        id_vehicle=db_vehicle.id_vehicle,
        number_plate=db_vehicle.number_plate,
        serial_number=db_vehicle.serial_number,
        year=db_vehicle.year,
        color=db_vehicle.color,
        km=db_vehicle.km,
        km_per_litre=db_vehicle.km_per_litre,
        id_model_fk=db_vehicle.id_model_fk,
        id_description_fk=db_vehicle.id_description_fk,
        id_brand_fk=db_vehicle.id_brand_fk,
        name_model=db_vehicle.model.name if db_vehicle.model else None,
        name_description=db_vehicle.description.name if db_vehicle.description else None,
        name_brand=db_vehicle.brand.name if db_vehicle.brand else None
      )
    return None

  def get_all_vehicles(self) -> list[VehicleOut]:
    db_vehicles = self.repo.get_all_vehicles()
    return [
      VehicleOut(
        id_vehicle=vehicle.id_vehicle,
        number_plate=vehicle.number_plate,
        serial_number=vehicle.serial_number,
        year=vehicle.year,
        color=vehicle.color,
        km=vehicle.km,
        km_per_litre=vehicle.km_per_litre,
        id_model_fk=vehicle.id_model_fk,
        id_description_fk=vehicle.id_description_fk,
        id_brand_fk=vehicle.id_brand_fk,
        name_model=vehicle.model.name if vehicle.model else None,
        name_description=vehicle.description.name if vehicle.description else None,
        name_brand=vehicle.brand.name if vehicle.brand else None
      ) for vehicle in db_vehicles
    ]

  def update_vehicle(self, vehicle_id: int, vehicle: VehicleUpdate) -> Optional[VehicleOut]:
  #   number_plate: Optional[str] = None
  # year: Optional[int] = None
  # color: Optional[str] = None
  # km: Optional[int] = None
  # route_status: Optional[vehicleRoute] = None
  # assignment_status: Optional[VehicleAssignmentStatus] = None
    db_vehicle = self.repo.get_vehicle_by_id(vehicle_id)
    if db_vehicle:
      if vehicle.number_plate is not None:
        db_vehicle.number_plate = vehicle.number_plate
      if vehicle.year is not None:
        db_vehicle.year = vehicle.year
      if vehicle.color is not None:
        db_vehicle.color = vehicle.color
      if vehicle.km is not None:
        db_vehicle.km = vehicle.km
      if vehicle.route_status is not None:
        db_vehicle.route_status = vehicle.route_status
      if vehicle.assignment_status is not None:
        db_vehicle.assignment_status = vehicle.assignment_status
        
      updated_vehicle = self.repo.update_vehicle(db_vehicle)
      return VehicleOut(
        id_vehicle=updated_vehicle.id_vehicle,
        number_plate=updated_vehicle.number_plate,
        serial_number=updated_vehicle.serial_number,
        year=updated_vehicle.year,
        color=updated_vehicle.color,
        km=updated_vehicle.km,
        km_per_litre=updated_vehicle.km_per_litre,
        id_model_fk=updated_vehicle.id_model_fk,
        id_description_fk=updated_vehicle.id_description_fk,
        id_brand_fk=updated_vehicle.id_brand_fk,
        name_model=updated_vehicle.model.name if updated_vehicle.model else None,
        name_description=updated_vehicle.description.name if updated_vehicle.description else None,
        name_brand=updated_vehicle.brand.name if updated_vehicle.brand else None
        
      )
    return None

  def delete_vehicle(self, vehicle_id: int) -> bool:
    db_vehicle = self.repo.get_vehicle_by_id(vehicle_id)
    if db_vehicle is not None:
      return self.repo.delete_vehicle(db_vehicle)
    return False

  def generate_vehicle_excel_report(self, vehicle_id: int) -> BytesIO:
    """
    Generate an Excel report for a vehicle with its routes and fuel stops
    
    Args:
        vehicle_id: The ID of the vehicle to report on
        
    Returns:
        BytesIO object containing the Excel file
    """
    # Get all data needed for the report
    vehicle, routes, fuel_stops_by_route = self.repo.get_vehicle_report_data(vehicle_id)
    
    if not vehicle:
        raise HTTPException(status_code=404, detail="Vehicle not found")
    
    # Generate Excel report
    excel_file = ExcelGenerator.generate_vehicle_report(
        vehicle=vehicle,
        routes=routes,
        fuel_stops_by_route=fuel_stops_by_route
    )
    
    return excel_file

  def get_vehicle_routes(self, vehicle_id: int) -> list[RouteOut]:
    """
    Get all routes for a specific vehicle
    
    Args:
        vehicle_id: ID of the vehicle
        
    Returns:
        List of routes for the vehicle
    """
    _, routes, _ = self.repo.get_vehicle_report_data(vehicle_id)
    
    # Convert Route models to RouteOut schemas
    return [
      RouteOut(
        id_route=route.id_route,
        id_vehicle_fk=route.id_vehicle_fk,
        id_user_fk=route.id_user_fk,
        description=route.description,
        latitude_start=route.latitude_start,
        longitude_start=route.longitude_start,
        latitude_end=route.latitude_end,
        longitude_end=route.longitude_end,
        start_time=route.start_time,
        end_time=route.end_time,
        estimated_time=route.estimated_time,
        total_duration=route.total_duration,
        on_time=route.on_time,
        start_km=route.start_km,
        end_km=route.end_km,
        estimated_km=route.estimated_km,
        image_start_km=route.image_start_km,
        image_end_km=route.image_end_km,
        on_distance=route.on_distance,
        liters_consumed=route.liters_consumed,
        name_vehicle=route.vehicle.number_plate if hasattr(route, 'vehicle') and route.vehicle else None,
        name_user=route.user.first_name + " " + route.user.last_name if hasattr(route, 'user') and route.user else None
      ) for route in routes
    ]
    
    
    
    
    
