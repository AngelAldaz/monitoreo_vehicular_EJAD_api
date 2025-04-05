from typing import Optional, Union
from app.schemas.fuelStopSchema import FuelStopCreate, FuelStopOut
from app.repositories.fuelStopRepository import FuelStopRepository
from app.models.fuelStopsModel import FuelStop

class FuelStopService:
    def __init__(self, fuel_stop_repo: FuelStopRepository) -> None:
        self.repo = fuel_stop_repo
        
    def _to_str(self, value: Union[str, float]) -> str:
        """Convierte valores numéricos a cadenas."""
        if isinstance(value, str):
            return value
        return str(value)

    def create_fuel_stop(self, fuel_stop: FuelStopCreate) -> FuelStopOut:
        db_fuel_stop = FuelStop(
            id_route_fk=fuel_stop.id_route_fk,
            Latitude_stop=self._to_str(fuel_stop.latitude_stop),
            Longitude_stop=self._to_str(fuel_stop.longitude_stop),
            stop_time=fuel_stop.stop_time,
            resume_time=fuel_stop.resume_time,
            start_time=fuel_stop.start_time,
            Latitude_start=self._to_str(fuel_stop.latitude_start) if fuel_stop.latitude_start else None,
            Longitude_start=self._to_str(fuel_stop.longitude_start) if fuel_stop.longitude_start else None,
            liters_added=fuel_stop.liters_added
        )
        created_fuel_stop = self.repo.create_fuel_stop(db_fuel_stop)
        return FuelStopOut(
            id_fuel_stop=created_fuel_stop.id_fuel_stop,
            id_route_fk=created_fuel_stop.id_route_fk,
            latitude_stop=created_fuel_stop.Latitude_stop,
            longitude_stop=created_fuel_stop.Longitude_stop,
            stop_time=created_fuel_stop.stop_time,
            resume_time=created_fuel_stop.resume_time,
            start_time=created_fuel_stop.start_time,
            latitude_start=created_fuel_stop.Latitude_start,
            longitude_start=created_fuel_stop.Longitude_start,
            liters_added=created_fuel_stop.liters_added,
            route_name=created_fuel_stop.route.description if created_fuel_stop.route else None
        )

    def get_fuel_stop_by_id(self, fuel_stop_id: int) -> Optional[FuelStopOut]:
        db_fuel_stop = self.repo.get_fuel_stop_by_id(fuel_stop_id)
        if db_fuel_stop is not None:
            return FuelStopOut(
                id_fuel_stop=db_fuel_stop.id_fuel_stop,
                id_route_fk=db_fuel_stop.id_route_fk,
                latitude_stop=db_fuel_stop.Latitude_stop,
                longitude_stop=db_fuel_stop.Longitude_stop,
                stop_time=db_fuel_stop.stop_time,
                resume_time=db_fuel_stop.resume_time,
                start_time=db_fuel_stop.start_time,
                latitude_start=db_fuel_stop.Latitude_start,
                longitude_start=db_fuel_stop.Longitude_start,
                liters_added=db_fuel_stop.liters_added,
                route_name=db_fuel_stop.route.description if db_fuel_stop.route else None
            )
        return None
    
    def get_fuel_stops_by_route_id(self, route_id: int) -> list[FuelStopOut]:
        db_fuel_stops = self.repo.get_fuel_stops_by_route_id(route_id)
        return [
            FuelStopOut(
                id_fuel_stop=fuel_stop.id_fuel_stop,
                id_route_fk=fuel_stop.id_route_fk,
                latitude_stop=fuel_stop.Latitude_stop,
                longitude_stop=fuel_stop.Longitude_stop,
                stop_time=fuel_stop.stop_time,
                resume_time=fuel_stop.resume_time,
                start_time=fuel_stop.start_time,
                latitude_start=fuel_stop.Latitude_start,
                longitude_start=fuel_stop.Longitude_start,
                liters_added=fuel_stop.liters_added,
                route_name=fuel_stop.route.description if fuel_stop.route else None
            ) for fuel_stop in db_fuel_stops
        ]
    
    def get_all_fuel_stops(self) -> list[FuelStopOut]:  
        db_fuel_stops = self.repo.get_all_fuel_stops()
        return [
            FuelStopOut(
                id_fuel_stop=fuel_stop.id_fuel_stop,
                id_route_fk=fuel_stop.id_route_fk,
                latitude_stop=fuel_stop.Latitude_stop,
                longitude_stop=fuel_stop.Longitude_stop,
                stop_time=fuel_stop.stop_time,
                resume_time=fuel_stop.resume_time,
                start_time=fuel_stop.start_time,
                latitude_start=fuel_stop.Latitude_start,
                longitude_start=fuel_stop.Longitude_start,
                liters_added=fuel_stop.liters_added,
                route_name=fuel_stop.route.description if fuel_stop.route else None
            ) for fuel_stop in db_fuel_stops
        ]
        
    def update_fuel_stop(self, fuel_stop_id: int, fuel_stop: FuelStopCreate) -> Optional[FuelStopOut]:
        db_fuel_stop = self.repo.get_fuel_stop_by_id(fuel_stop_id)
        if db_fuel_stop is not None:
            db_fuel_stop.id_route_fk = fuel_stop.id_route_fk
            db_fuel_stop.Latitude_stop = self._to_str(fuel_stop.latitude_stop)
            db_fuel_stop.Longitude_stop = self._to_str(fuel_stop.longitude_stop)
            db_fuel_stop.stop_time = fuel_stop.stop_time
            db_fuel_stop.resume_time = fuel_stop.resume_time
            db_fuel_stop.start_time = fuel_stop.start_time
            db_fuel_stop.Latitude_start = self._to_str(fuel_stop.latitude_start) if fuel_stop.latitude_start else None
            db_fuel_stop.Longitude_start = self._to_str(fuel_stop.longitude_start) if fuel_stop.longitude_start else None
            db_fuel_stop.liters_added = fuel_stop.liters_added
            updated_fuel_stop = self.repo.update_fuel_stop(db_fuel_stop)
            return FuelStopOut(
                id_fuel_stop=updated_fuel_stop.id_fuel_stop,
                id_route_fk=updated_fuel_stop.id_route_fk,
                latitude_stop=updated_fuel_stop.Latitude_stop,
                longitude_stop=updated_fuel_stop.Longitude_stop,
                stop_time=updated_fuel_stop.stop_time,
                resume_time=updated_fuel_stop.resume_time,
                start_time=updated_fuel_stop.start_time,
                latitude_start=updated_fuel_stop.Latitude_start,
                longitude_start=updated_fuel_stop.Longitude_start,
                liters_added=updated_fuel_stop.liters_added,
                route_name=updated_fuel_stop.route.description if updated_fuel_stop.route else None
            )
        return None
    
    def delete_fuel_stop(self, fuel_stop_id: int) -> bool:
        db_fuel_stop = self.repo.get_fuel_stop_by_id(fuel_stop_id)
        if db_fuel_stop is not None:
            return self.repo.delete_fuel_stop(db_fuel_stop)
        return False
        
    
    


