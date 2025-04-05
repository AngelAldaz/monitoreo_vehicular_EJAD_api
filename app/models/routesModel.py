from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean, Double
from sqlalchemy.orm import relationship
from app.database import Base

class Route(Base):
    __tablename__ = "Route"

    id_route = Column(Integer, primary_key=True, index=True, autoincrement=True)
    id_vehicle_fk = Column(Integer, ForeignKey("Vehicle.id_vehicle"), nullable=False)
    id_user_fk = Column(Integer, ForeignKey("User.id_usuario"), nullable=False)
    description = Column(String(255), nullable=False)
   
    latitude_start = Column(String(50), nullable=True)
    longitude_start = Column(String(50), nullable=True)
    
    latitude_end = Column(String(50), nullable=True)
    longitude_end = Column(String(50), nullable=True)
    
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=False)
    estimated_time = Column(Double, nullable=False)
    total_duration = Column(Double, nullable=False)
    on_time = Column(Boolean)

    start_km = Column(Integer, nullable=False)
    end_km = Column(Integer, nullable=False)
    estimated_km = Column(Integer, nullable=False)
    image_start_km = Column(String(255), nullable=True)  # Ruta de la imagen
    image_end_km = Column(String(255), nullable=True)  # Ruta de la imagen
    on_distance = Column(Boolean)
    
    liters_consumed = Column(Double, nullable=False)
    
    vehicle = relationship("Vehicle", back_populates="routes")
    user = relationship("User", back_populates="routes")
    fuel_stops = relationship("FuelStop", back_populates="route")
    

    
    
    
    
