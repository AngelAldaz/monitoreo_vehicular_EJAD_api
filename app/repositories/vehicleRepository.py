from sqlalchemy.orm import Session, joinedload
from app.models.vehiclesModel import Vehicle
from app.models.modelsModel import Model
from app.models.brandsModel import Brand
from app.models.descriptionsModel import Description
from app.models.routesModel import Route
from app.models.fuelStopsModel import FuelStop
from app.models.usersModel import User


class VehicleRepository:
  def __init__(self, db: Session) -> None:
    self.db = db
    
  def create_vehicle(self, vehicle: Vehicle) -> Vehicle:
    self.db.add(vehicle)
    self.db.commit()
    self.db.refresh(vehicle)
    self.db.refresh(vehicle, attribute_names=['model', 'brand', 'description'])
    return vehicle

  def get_vehicle_by_id(self, vehicle_id: int) -> Vehicle:
    result = self.db.query(Vehicle).options(joinedload(Vehicle.model), joinedload(Vehicle.brand), joinedload(Vehicle.description)).filter(Vehicle.id_vehicle == vehicle_id)
    return result.first()

  def get_all_vehicles(self) -> list[Vehicle]:
    return self.db.query(Vehicle).options(joinedload(Vehicle.model), joinedload(Vehicle.brand), joinedload(Vehicle.description)).all()

  def update_vehicle(self, vehicle: Vehicle) -> Vehicle:
    self.db.merge(vehicle)
    self.db.commit()
    self.db.refresh(vehicle)
    self.db.refresh(vehicle, attribute_names=['model', 'brand', 'description'])
    return vehicle

  def delete_vehicle(self, vehicle: Vehicle) -> bool:
    self.db.delete(vehicle)
    self.db.commit()
    return True

  def get_vehicle_report_data(self, vehicle_id: int) -> tuple:
    """
    Get a vehicle with all its routes and fuel stops for a report
    
    Args:
        vehicle_id: The ID of the vehicle to report on
        
    Returns:
        Tuple containing (vehicle, routes, fuel_stops_by_route)
    """
    vehicle = self.get_vehicle_by_id(vehicle_id)
    if not vehicle:
        return None, [], {}
    
    # Get all routes for this vehicle with relationships loaded
    routes = self.db.query(Route).options(
        joinedload(Route.user),
        joinedload(Route.vehicle)
    ).filter(Route.id_vehicle_fk == vehicle_id).all()
    
    # Get all fuel stops for each route with route relationship loaded
    fuel_stops_by_route = {}
    for route in routes:
        fuel_stops = self.db.query(FuelStop).options(
            joinedload(FuelStop.route)
        ).filter(FuelStop.id_route_fk == route.id_route).all()
        fuel_stops_by_route[route.id_route] = fuel_stops
    
    return vehicle, routes, fuel_stops_by_route
    