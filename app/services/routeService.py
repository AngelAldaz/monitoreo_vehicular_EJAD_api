from typing import Optional, Union
from app.schemas.routesSchema import RouteCreate, RouteOut
from app.repositories.routeRepository import RouteRepository
from app.models.routesModel import Route

class RouteService:
    def __init__(self, route_repo: RouteRepository) -> None:
        self.repo = route_repo

    def _to_bool(self, value: Union[bool, int]) -> bool:
        """Convierte valores enteros a booleanos (0 = False, cualquier otro número = True)."""
        if isinstance(value, bool):
            return value
        return bool(value)
    
    def _to_str(self, value: Union[str, float]) -> str:
        """Convierte valores numéricos a cadenas."""
        if isinstance(value, str):
            return value
        return str(value)

    def create_route(self, route: RouteCreate) -> RouteOut:
        db_route = Route(
            id_vehicle_fk=route.id_vehicle_fk,
            id_user_fk=route.id_user_fk,
            description=route.description,
            latitude_start=self._to_str(route.latitude_start),
            longitude_start=self._to_str(route.longitude_start),
            latitude_end=self._to_str(route.latitude_end),
            longitude_end=self._to_str(route.longitude_end),
            start_time=route.start_time,
            end_time=route.end_time,
            estimated_time=route.estimated_time,
            total_duration=route.total_duration,
            on_time=self._to_bool(route.on_time),
            start_km=route.start_km,
            end_km=route.end_km,
            estimated_km=route.estimated_km,
            image_start_km=route.image_start_km,
            image_end_km=route.image_end_km,
            on_distance=self._to_bool(route.on_distance),
            liters_consumed=route.liters_consumed
        )
        created_route = self.repo.create_route(db_route)
        return RouteOut(
            id_route=created_route.id_route,
            id_vehicle_fk=created_route.id_vehicle_fk,
            id_user_fk=created_route.id_user_fk,
            description=created_route.description,
            latitude_start=created_route.latitude_start,
            longitude_start=created_route.longitude_start,
            latitude_end=created_route.latitude_end,
            longitude_end=created_route.longitude_end,
            start_time=created_route.start_time,
            end_time=created_route.end_time,
            estimated_time=created_route.estimated_time,
            total_duration=created_route.total_duration,
            on_time=created_route.on_time,
            start_km=created_route.start_km,
            end_km=created_route.end_km,
            estimated_km=created_route.estimated_km,
            image_start_km=created_route.image_start_km,
            image_end_km=created_route.image_end_km,
            on_distance=created_route.on_distance,
            liters_consumed=created_route.liters_consumed,
            name_vehicle=created_route.vehicle.number_plate if created_route.vehicle else None,
            name_user=created_route.user.first_name if created_route.user else None
        )

    def get_route_by_id(self, route_id: int) -> Optional[RouteOut]:
        db_route = self.repo.get_route_by_id(route_id)
        if db_route is not None:
            return RouteOut(
                id_route=db_route.id_route,
                id_vehicle_fk=db_route.id_vehicle_fk,
                id_user_fk=db_route.id_user_fk,
                description=db_route.description,
                latitude_start=db_route.latitude_start,
                longitude_start=db_route.longitude_start,
                latitude_end=db_route.latitude_end,
                longitude_end=db_route.longitude_end,
                start_time=db_route.start_time,
                end_time=db_route.end_time,
                estimated_time=db_route.estimated_time,
                total_duration=db_route.total_duration,
                on_time=db_route.on_time,
                start_km=db_route.start_km,
                end_km=db_route.end_km,
                estimated_km=db_route.estimated_km,
                image_start_km=db_route.image_start_km,
                image_end_km=db_route.image_end_km,
                on_distance=db_route.on_distance,
                liters_consumed=db_route.liters_consumed,
                name_vehicle=db_route.vehicle.number_plate if db_route.vehicle else None,
                name_user=db_route.user.first_name if db_route.user else None
            )
        return None
    
    def get_all_routes(self) -> list[RouteOut]:
        db_routes = self.repo.get_all_routes()
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
                name_vehicle=route.vehicle.number_plate if route.vehicle else None,
                name_user=route.user.first_name if route.user else None
            ) for route in db_routes
        ]
    
    def update_route(self, route_id: int, route: RouteCreate) -> Optional[RouteOut]:
        db_route = self.repo.get_route_by_id(route_id)
        if db_route is not None:
            db_route.id_vehicle_fk = route.id_vehicle_fk
            db_route.id_user_fk = route.id_user_fk
            db_route.description = route.description
            db_route.latitude_start = self._to_str(route.latitude_start)
            db_route.longitude_start = self._to_str(route.longitude_start)
            db_route.latitude_end = self._to_str(route.latitude_end)
            db_route.longitude_end = self._to_str(route.longitude_end)
            db_route.start_time = route.start_time
            db_route.end_time = route.end_time
            db_route.estimated_time = route.estimated_time
            db_route.total_duration = route.total_duration
            db_route.on_time = self._to_bool(route.on_time)
            db_route.start_km = route.start_km
            db_route.end_km = route.end_km
            db_route.estimated_km = route.estimated_km
            db_route.image_start_km = route.image_start_km
            db_route.image_end_km = route.image_end_km
            db_route.on_distance = self._to_bool(route.on_distance)
            db_route.liters_consumed = route.liters_consumed
            updated_route = self.repo.update_route(db_route)
            return RouteOut(
                id_route=updated_route.id_route,
                id_vehicle_fk=updated_route.id_vehicle_fk,
                id_user_fk=updated_route.id_user_fk,
                description=updated_route.description,
                latitude_start=updated_route.latitude_start,
                longitude_start=updated_route.longitude_start,
                latitude_end=updated_route.latitude_end,
                longitude_end=updated_route.longitude_end,
                start_time=updated_route.start_time,
                end_time=updated_route.end_time,
                estimated_time=updated_route.estimated_time,
                total_duration=updated_route.total_duration,
                on_time=updated_route.on_time,
                start_km=updated_route.start_km,
                end_km=updated_route.end_km,
                estimated_km=updated_route.estimated_km,
                image_start_km=updated_route.image_start_km,
                image_end_km=updated_route.image_end_km,
                on_distance=updated_route.on_distance,
                liters_consumed=updated_route.liters_consumed,  
                name_vehicle=updated_route.vehicle.number_plate if updated_route.vehicle else None,
                name_user=updated_route.user.first_name if updated_route.user else None
            )
        return None
    
    def delete_route(self, route_id: int) -> bool:
        db_route = self.repo.get_route_by_id(route_id)
        if db_route is not None:
            return self.repo.delete_route(db_route)
        return False
    
                
            
            
            
    
            
            
