from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean, Double
from sqlalchemy.orm import relationship
from app.database import Base

class Route(Base):
    __tablename__ = "Route"

    id_route = Column(Integer, primary_key=True, index=True, autoincrement=True)
    id_vehicle_fk = Column(Integer, ForeignKey("Vehicle.id_vehicle"), nullable=False)
    
    description = Column(String(255), nullable=False)
   
    
    Latitude_start = Column(String(255), nullable=True)
    Longitude_start = Column(String(255), nullable=True)
    
    Latitude_end = Column(String(255), nullable=True)
    Longitude_end = Column(String(255), nullable=True)
    
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=False)
    estimated_time = Column(Double, nullable=False)
    total_duration = Column(Double, nullable=False)
    on_time = Column(Boolean)

    start_km = Column(Integer, nullable=False)
    end_km = Column(Integer, nullable=False)
    stimated_km = Column(Integer, nullable=False)
    image_start_km = Column(String(255), nullable=True)  # Ruta de la imagen
    image_end_km = Column(String(255), nullable=True)  # Ruta de la imagen
    on_distance = Column(Boolean)
    
    Latitude_start = Column(String(255), nullable=True)
    Longitude_star = Column(String(255), nullable=True)
    
    
    liters_consumed = Column(Double, nullable=False)
    
    id_vehicle_fk = Column(Integer, ForeignKey("Vehicle.id_vehicle"), nullable=False)
    id_lider_fk= Column(Integer, ForeignKey("User.id_user"), nullable=False)
    
    
    
    
    
