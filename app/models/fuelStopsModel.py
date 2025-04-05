from sqlalchemy import Column, Integer, String, DateTime, DECIMAL, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.hybrid import hybrid_property
from app.database import Base
from datetime import datetime

class FuelStop(Base):
    __tablename__ = "FuelStop"

    id_fuel_stop = Column(Integer, primary_key=True, index=True, autoincrement=True)
    id_route_fk = Column(Integer, ForeignKey("Route.id_route"), nullable=False)
    
    Latitude_stop = Column(String(255), nullable=False)
    Longitude_stop = Column(String(255), nullable=False)
    stop_time = Column(DateTime, nullable=False)
    
    resume_time = Column(DateTime, nullable=True)
    
    start_time = Column(DateTime, nullable=True)
    Latitude_start = Column(String(255), nullable=True)
    Longitude_start = Column(String(255), nullable=True)
    
    current_km = Column(Integer, nullable=True)
    image_km = Column(String(255), nullable=True)
    
    liters_added = Column(DECIMAL(5, 2), nullable=False)

    # Relación con la tabla Route
    route = relationship("Route", back_populates="fuel_stops")

    # Propiedad para obtener información de la ruta relacionada
    @hybrid_property
    def route_name(self):
        return self.route.description if self.route else None 