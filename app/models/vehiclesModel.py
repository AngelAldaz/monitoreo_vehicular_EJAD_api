from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.hybrid import hybrid_property
from app.database import Base
from app.models.modelsModel import Model
from app.models.descriptionsModel import Description
from app.models.brandsModel import Brand

from sqlalchemy import Enum
from app.models.vehicleRoute import vehicleRoute
from app.models.VehicleAssignmentStatus import VehicleAssignmentStatus


class Vehicle(Base):
    __tablename__ = "Vehicle"

    id_vehicle = Column(Integer, primary_key=True, index=True, autoincrement=True)
    
    id_model_fk = Column(Integer, ForeignKey("Model.id_model"), nullable=False)
    id_description_fk = Column(Integer, ForeignKey("Description.id_description"), nullable=False)
    id_brand_fk = Column(Integer, ForeignKey("Brand.id_brand"), nullable=False)
    
    number_plate = Column(String(10), nullable=False)
    serial_number = Column(String(10), nullable=False)
    
    year = Column(Integer, nullable=False)
    color = Column(String(20), nullable=False)
    
    km = Column(Integer, nullable=False)
    km_per_litre = Column(Integer, nullable=False)
    
    
    
    
    model = relationship("Model", back_populates="vehicles")
    description = relationship("Description", back_populates="vehicles")
    brand = relationship("Brand", back_populates="vehicles")
    
    
    
    route_status = Column(Enum(vehicleRoute), default=vehicleRoute.OFF_ROUTE)
    assignment_status = Column(Enum(VehicleAssignmentStatus),  default=VehicleAssignmentStatus.NOT_ASSIGNED)

    
    
    
    
    
    #Falta el id de user
    

    # Propiedad para obtener el nombre del modelo
    @hybrid_property
    def model_name(self):
        return self.model.name if self.model else None

    # Propiedad para obtener el nombre de la descripción
    @hybrid_property
    def description_name(self):
        return self.description.name if self.description else None


    # Propiedad para obtener el nombre de la marca
    @hybrid_property
    def brand_name(self):
        return self.brand.name if self.brand else None  



