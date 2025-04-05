from sqlalchemy.orm import Session, joinedload
from typing import List
from app.models.routesModel import Route
from app.models.vehiclesModel import Vehicle
from app.models.usersModel import User


class RouteRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_route(self, route: Route) -> Route:
        self.db.add(route)
        self.db.commit()
        self.db.refresh(route)
        self.db.refresh(route, attribute_names=["vehicle", "user"])
        return route
    
    def get_route_by_id(self, route_id: int) -> Route:
        result = self.db.query(Route).options(
            joinedload(Route.vehicle),
            joinedload(Route.user)
        ).filter(Route.id_route == route_id).first()
        return result
    
    def get_all_routes(self) -> List[Route]:
        return self.db.query(Route).options(
            joinedload(Route.vehicle),
            joinedload(Route.user)
        ).all()
        
    def update_route(self, route: Route) -> Route:
        self.db.merge(route)
        self.db.commit()
        self.db.refresh(route)
        self.db.refresh(route, attribute_names=["vehicle", "user"])
        return route
    
    def delete_route(self, route: Route) -> bool:
        self.db.delete(route)
        self.db.commit()
        return True 
    
    
    
    
    
