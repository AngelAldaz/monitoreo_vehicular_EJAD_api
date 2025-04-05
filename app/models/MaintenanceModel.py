from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.hybrid import hybrid_property
from app.database import Base
from datetime import datetime
from sqlalchemy import Enum
from app.models.MaintenanceStatus import MaintenanceStatus


class Maintenance(Base):
    __tablename__ = "Maintenance"

    # Campos
    id_maintenance = Column(Integer, primary_key=True, index=True, autoincrement=True)
    id_vehicle_fk = Column(Integer, ForeignKey("Vehicle.id_vehicle"), nullable=False)
    
    description = Column(Text, nullable=True)
    
    start_time = Column(DateTime, nullable=False)
    estimated_time = Column(Time, nullable=False)
    end_time = Column(DateTime, nullable=True)
    
    status = Column(Enum(MaintenanceStatus), nullable=False)

    #Model usuario faltante 
   
    
    
    
    
