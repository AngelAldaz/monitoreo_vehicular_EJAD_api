from sqlalchemy.orm import Session, joinedload
from app.models.fuelStopsModel import FuelStop
from app.models.routesModel import Route


class FuelStopRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def create_fuel_stop(self, fuel_stop: FuelStop) -> FuelStop:
        self.db.add(fuel_stop)
        self.db.commit()
        self.db.refresh(fuel_stop)
        self.db.refresh(fuel_stop, attribute_names=['route'])
        return fuel_stop
    
    def get_fuel_stop_by_id(self, fuel_stop_id: int) -> FuelStop:
        result = self.db.query(FuelStop).options(joinedload(FuelStop.route)).filter(FuelStop.id_fuel_stop == fuel_stop_id)
        return result.first()
    
    def get_fuel_stops_by_route_id(self, route_id: int) -> list[FuelStop]:
        return self.db.query(FuelStop).options(joinedload(FuelStop.route)).filter(FuelStop.id_route_fk == route_id).all()
    
    def get_all_fuel_stops(self) -> list[FuelStop]:
        return self.db.query(FuelStop).options(joinedload(FuelStop.route)).all()
    
    def update_fuel_stop(self, fuel_stop: FuelStop) -> FuelStop:
        self.db.merge(fuel_stop)
        self.db.commit()
        self.db.refresh(fuel_stop)
        self.db.refresh(fuel_stop, attribute_names=['route'])
        return fuel_stop
    
    def delete_fuel_stop(self, fuel_stop: FuelStop) -> bool:
        self.db.delete(fuel_stop)
        self.db.commit()
        return True
    
