from typing import Optional, Union
from app.schemas.routesSchema import RouteCreate, RouteOut, RouteStartSchema, RouteStartResponse, RouteEndSchema, RouteEndResponse
from app.repositories.routeRepository import RouteRepository
from app.repositories.vehicleRepository import VehicleRepository
from app.models.routesModel import Route
from app.models.vehicleRoute import vehicleRoute
from datetime import datetime, timedelta
from fastapi import HTTPException
from app.utils.distanceUtil import calculate_distance
from datetime import datetime, timezone

class RouteService:
    def __init__(self, route_repo: RouteRepository, vehicle_repo: VehicleRepository = None) -> None:
        self.repo = route_repo
        self.vehicle_repo = vehicle_repo

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
    
    def start_route(self, route_start: RouteStartSchema) -> RouteStartResponse:
        """
        Start a new route with minimal information and set vehicle status to ON_ROUTE
        
        Args:
            route_start: Basic information to start a route
            
        Returns:
            A RouteStartResponse with the created route information
        """
        # Create a new route with default values for required fields
        estimated_time = 0.0  # Default value
        end_time = route_start.start_time + timedelta(hours=8)  # Default end time (8 hours later)
        
        vehicle = self.vehicle_repo.get_vehicle_by_id(route_start.id_vehicle_fk)
        if vehicle.route_status == vehicleRoute.ON_ROUTE:
            raise HTTPException(status_code=400, detail="Vehicle is already on route")
        
        db_route = Route(
            id_vehicle_fk=route_start.id_vehicle_fk,
            id_user_fk=route_start.id_user_fk,
            description=route_start.description,
            latitude_start=self._to_str(route_start.latitude_start),
            longitude_start=self._to_str(route_start.longitude_start),
            latitude_end="0",  # Default value
            longitude_end="0",  # Default value
            start_time=route_start.start_time,
            end_time=end_time,
            estimated_time=estimated_time,
            total_duration=0.0,  # Default value
            on_time=False,  # Default value
            start_km=route_start.start_km,
            end_km=0,  # Default value
            estimated_km=0,  # Default value 
            image_start_km=route_start.image_start_km,
            image_end_km="",  # Default value
            on_distance=False,  # Default value
            liters_consumed=0.0  # Default value
        )
        
        created_route = self.repo.create_route(db_route)
        
        # Update vehicle status to ON_ROUTE if vehicle_repo is provided
        if self.vehicle_repo and created_route:
            vehicle = self.vehicle_repo.get_vehicle_by_id(route_start.id_vehicle_fk)
            if vehicle:
                vehicle.route_status = vehicleRoute.ON_ROUTE
                self.vehicle_repo.update_vehicle(vehicle)
        
        return RouteStartResponse(
            id_route=created_route.id_route,
            id_vehicle_fk=created_route.id_vehicle_fk,
            id_user_fk=created_route.id_user_fk,
            description=created_route.description,
            latitude_start=created_route.latitude_start,
            longitude_start=created_route.longitude_start,
            start_time=created_route.start_time,
            start_km=created_route.start_km,
            image_start_km=created_route.image_start_km,
            name_vehicle=created_route.vehicle.number_plate if created_route.vehicle else None,
            name_user=created_route.user.first_name if created_route.user else None
        )
    
    def end_route(self, route_end: RouteEndSchema) -> RouteEndResponse:
        # """
        # Start a new route with minimal information and set vehicle status to ON_ROUTE
        
        # Args:
        #     route_start: Basic information to start a route
            
        # Returns:
        #     A RouteStartResponse with the created route information
        # """
        # route_db = self.repo.get_route_by_id(route_end.id_route)
        # # Create a new route with default values for required fields
        # distance_approx, estimated_time = calculate_distance(float(route_db.latitude_start), float(route_db.longitude_start), float(route_end.latitude_end), float(route_end.longitude_end))
        # # estimated_time = 0.0  # Default value
        # start_time = route_db.start_time.replace(tzinfo=timezone.utc)
        # end_time = route_end.end_time.astimezone(timezone.utc)
        # total_duration = end_time - start_time
        # # In your code before saving, convert the timedelta to seconds
        # total_duration_seconds = total_duration.total_seconds() // 3600
        
        # vehicle = self.vehicle_repo.get_vehicle_by_id(route_end.id_vehicle_fk)
        # if vehicle.route_status != vehicleRoute.ON_ROUTE:
        #     raise HTTPException(status_code=400, detail="Vehicle not on route")
        
        # db_route = Route(
        #     id_vehicle_fk=route_end.id_vehicle_fk,
        #     id_user_fk=route_end.id_user_fk,
        #     description=route_end.description,
        #     latitude_start=self._to_str(route_db.latitude_start),
        #     longitude_start=self._to_str(route_db.longitude_start),
        #     latitude_end=self._to_str(route_end.latitude_end),  # Default value
        #     longitude_end=self._to_str(route_end.longitude_end),
        #     start_time=route_db.start_time,
        #     end_time=end_time,
        #     estimated_time=estimated_time,
        #     total_duration= total_duration_seconds,  # Default value
        #     on_time= total_duration_seconds <= total_duration_seconds*1.2,  # Default value
        #     start_km=route_db.start_km,
        #     end_km=route_end.end_km,
        #     estimated_km=distance_approx,
        #     image_start_km=route_db.image_start_km,
        #     image_end_km=route_end.image_end_km,
        #     on_distance= (route_end.end_km - route_db.start_km) <= (distance_approx + 5),  # Default value
        #     liters_consumed=vehicle.km_per_litre*(route_end.end_km-route_db.start_km)  # Default value
        # )
        
        # updated_route = self.repo.update_route(db_route)
        
        # # Update vehicle status to ON_ROUTE if vehicle_repo is provided
        # vehicle.route_status = vehicleRoute.OFF_ROUTE
        # self.vehicle_repo.update_vehicle(vehicle)
        
        # return RouteEndResponse(
        #     id_route=updated_route.id_route,
        #     id_vehicle_fk=updated_route.id_vehicle_fk,
        #     id_user_fk=updated_route.id_user_fk,
        #     description=updated_route.description,
        #     latitude_start=updated_route.latitude_start,
        #     longitude_start=updated_route.longitude_start,
        #     start_time=updated_route.start_time,
        #     start_km=updated_route.start_km,
        #     image_start_km=updated_route.image_start_km,
        #     name_vehicle=updated_route.vehicle.number_plate if updated_route.vehicle else None,
        #     name_user=updated_route.user.first_name if updated_route.user else None,
        #     latitude_end= updated_route.latitude_end,
        #     longitude_end = updated_route.longitude_end,
        #     end_time = updated_route.end_time,
        #     end_km = updated_route.end_km,
        #     image_end_km = updated_route.image_end_km,
        #     route_status = vehicleRoute.OFF_ROUTE.value
        # )
        """
        Complete an existing route and set vehicle status to OFF_ROUTE
        
        Args:
            route_end: Information to complete a route
            
        Returns:
            A RouteEndResponse with the completed route information
        """
        route_db = self.repo.get_route_by_id(route_end.id_route)
        if not route_db:
            raise HTTPException(status_code=404, detail="Route not found")

        # Calculate route metrics
        distance_approx, estimated_time = calculate_distance(
            float(route_db.latitude_start), 
            float(route_db.longitude_start), 
            float(route_end.latitude_end), 
            float(route_end.longitude_end)
        )
        
        # Calculate duration
        start_time = route_db.start_time.replace(tzinfo=timezone.utc)
        end_time = route_end.end_time.astimezone(timezone.utc)
        total_duration = (end_time - start_time).total_seconds() / 3600  # in hours
        
        # Get vehicle info
        vehicle = self.vehicle_repo.get_vehicle_by_id(route_end.id_vehicle_fk)
        if not vehicle:
            raise HTTPException(status_code=404, detail="Vehicle not found")
        if vehicle.route_status != vehicleRoute.ON_ROUTE:
            raise HTTPException(status_code=400, detail="Vehicle not on route")

        # Update the existing route object
        route_db.description = route_end.description
        route_db.latitude_end = self._to_str(route_end.latitude_end)
        route_db.longitude_end = self._to_str(route_end.longitude_end)
        route_db.end_time = end_time
        route_db.estimated_time = estimated_time
        route_db.total_duration = total_duration
        route_db.on_time = total_duration <= estimated_time * 1.2  # 20% tolerance
        route_db.end_km = route_end.end_km
        route_db.estimated_km = distance_approx
        route_db.image_end_km = route_end.image_end_km
        route_db.on_distance = (route_end.end_km - route_db.start_km) <= (distance_approx + 5)
        route_db.liters_consumed = vehicle.km_per_litre * (route_end.end_km - route_db.start_km)

        # Update vehicle status
        vehicle.route_status = vehicleRoute.OFF_ROUTE
        self.vehicle_repo.update_vehicle(vehicle)

        # Save changes
        updated_route = self.repo.update_route(route_db)
        
        return RouteEndResponse(
            id_route=updated_route.id_route,
            id_vehicle_fk=updated_route.id_vehicle_fk,
            id_user_fk=updated_route.id_user_fk,
            description=updated_route.description,
            latitude_start=updated_route.latitude_start,
            longitude_start=updated_route.longitude_start,
            start_time=updated_route.start_time,
            start_km=updated_route.start_km,
            image_start_km=updated_route.image_start_km,
            name_vehicle=updated_route.vehicle.number_plate if updated_route.vehicle else None,
            name_user=updated_route.user.first_name if updated_route.user else None,
            latitude_end=updated_route.latitude_end,
            longitude_end=updated_route.longitude_end,
            end_time=updated_route.end_time,
            end_km=updated_route.end_km,
            image_end_km=updated_route.image_end_km,
            route_status=vehicleRoute.OFF_ROUTE.value
        )