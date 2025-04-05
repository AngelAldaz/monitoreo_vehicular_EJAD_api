from typing import Optional, Union
from app.schemas.fuelStopSchema import (
    FuelStopCreate, FuelStopOut, FuelStopStartSchema, 
    FuelStopStartResponse, FuelStopFinishSchema, FuelStopFinishResponse
)
from app.repositories.fuelStopRepository import FuelStopRepository
from app.repositories.vehicleRepository import VehicleRepository
from app.repositories.routeRepository import RouteRepository
from app.models.fuelStopsModel import FuelStop
from app.models.vehicleRoute import vehicleRoute
from fastapi import HTTPException

class FuelStopService:
    def __init__(self, fuel_stop_repo: FuelStopRepository, vehicle_repo: VehicleRepository = None, route_repo: RouteRepository = None) -> None:
        self.repo = fuel_stop_repo
        self.vehicle_repo = vehicle_repo
        self.route_repo = route_repo
        
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
    
    def start_refueling(self, fuel_stop_data: FuelStopStartSchema) -> FuelStopStartResponse:
        """
        Inicia una parada para reabastecimiento de combustible y cambia el estado del vehículo a REFUELING
        
        Args:
            fuel_stop_data: Datos básicos para iniciar una parada de combustible
            
        Returns:
            FuelStopStartResponse con la información de la parada creada
        """
        # Creamos la parada de combustible con valores por defecto para campos requeridos
        db_fuel_stop = FuelStop(
            id_route_fk=fuel_stop_data.id_route_fk,
            Latitude_stop=self._to_str(fuel_stop_data.latitude_stop),
            Longitude_stop=self._to_str(fuel_stop_data.longitude_stop),
            stop_time=fuel_stop_data.stop_time,
            resume_time=None,
            start_time=None,
            Latitude_start=None,
            Longitude_start=None,
            liters_added=0.0  # Valor por defecto que se actualizará al finalizar la carga
        )
        
        created_fuel_stop = self.repo.create_fuel_stop(db_fuel_stop)
        
        # Cambiar el estado del vehículo a REFUELING si tenemos acceso al repositorio de vehículos
        vehicle_status = ""
        if self.vehicle_repo and self.route_repo and created_fuel_stop:
            # Obtener la ruta para saber qué vehículo está involucrado
            route = self.route_repo.get_route_by_id(fuel_stop_data.id_route_fk)
            if route:
                vehicle = self.vehicle_repo.get_vehicle_by_id(route.id_vehicle_fk)
                if vehicle:
                    # Verificar que el vehículo esté en estado ON_ROUTE
                    if vehicle.route_status != vehicleRoute.ON_ROUTE:
                        raise HTTPException(status_code=400, detail="Vehicle is not in ON_ROUTE state")
                    
                    # Actualizar el estado del vehículo a REFUELING
                    vehicle.route_status = vehicleRoute.REFUELING
                    self.vehicle_repo.update_vehicle(vehicle)
                    vehicle_status = vehicleRoute.REFUELING.value
        
        return FuelStopStartResponse(
            id_fuel_stop=created_fuel_stop.id_fuel_stop,
            id_route_fk=created_fuel_stop.id_route_fk,
            latitude_stop=created_fuel_stop.Latitude_stop,
            longitude_stop=created_fuel_stop.Longitude_stop,
            stop_time=created_fuel_stop.stop_time,
            route_name=created_fuel_stop.route.description if created_fuel_stop.route else None,
            vehicle_status=vehicle_status
        )
        
    def finish_refueling(self, fuel_stop_data: FuelStopFinishSchema) -> FuelStopFinishResponse:
        """
        Finaliza una parada de reabastecimiento de combustible y cambia el estado del vehículo de vuelta a ON_ROUTE
        
        Args:
            fuel_stop_data: Datos para finalizar una parada de combustible
            
        Returns:
            FuelStopFinishResponse con la información completa de la parada
        """
        # Obtener la parada de combustible existente
        db_fuel_stop = self.repo.get_fuel_stop_by_id(fuel_stop_data.id_fuel_stop)
        if not db_fuel_stop:
            raise HTTPException(status_code=404, detail="Fuel stop not found")
        
        # Actualizar datos de la parada de combustible
        db_fuel_stop.resume_time = fuel_stop_data.resume_time
        db_fuel_stop.start_time = fuel_stop_data.start_time
        db_fuel_stop.Latitude_start = self._to_str(fuel_stop_data.latitude_start)
        db_fuel_stop.Longitude_start = self._to_str(fuel_stop_data.longitude_start)
        db_fuel_stop.liters_added = fuel_stop_data.liters_added
        db_fuel_stop.current_km = fuel_stop_data.current_km
        db_fuel_stop.image_km = fuel_stop_data.image_km
        
        updated_fuel_stop = self.repo.update_fuel_stop(db_fuel_stop)
        
        # Cambiar el estado del vehículo de vuelta a ON_ROUTE
        vehicle_status = ""
        if self.vehicle_repo and self.route_repo and updated_fuel_stop:
            # Obtener la ruta para saber qué vehículo está involucrado
            route = self.route_repo.get_route_by_id(updated_fuel_stop.id_route_fk)
            if route:
                vehicle = self.vehicle_repo.get_vehicle_by_id(route.id_vehicle_fk)
                if vehicle:
                    # Verificar que el vehículo esté en estado REFUELING
                    if vehicle.route_status != vehicleRoute.REFUELING:
                        raise HTTPException(status_code=400, detail="Vehicle is not in REFUELING state")
                    
                    # Actualizar el estado del vehículo a ON_ROUTE
                    vehicle.route_status = vehicleRoute.ON_ROUTE
                    # Actualizar el kilometraje del vehículo
                    vehicle.km = fuel_stop_data.current_km
                    self.vehicle_repo.update_vehicle(vehicle)
                    vehicle_status = vehicleRoute.ON_ROUTE.value
        
        return FuelStopFinishResponse(
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
            current_km=updated_fuel_stop.current_km,
            image_km=updated_fuel_stop.image_km,
            route_name=updated_fuel_stop.route.description if updated_fuel_stop.route else None,
            vehicle_status=vehicle_status
        )
        
    
    


