from sqlalchemy.orm import Session, joinedload
from app.models.vehiclesModel import Vehicle
from app.models.modelsModel import Model
from app.models.brandsModel import Brand
from app.models.descriptionsModel import Description


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
    