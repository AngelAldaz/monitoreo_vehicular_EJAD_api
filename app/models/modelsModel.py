from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class Model(Base):
    __tablename__ = "Model"

    id_model = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    
    id_brand_fk = Column(Integer, ForeignKey("Brand.id_brand"), nullable=False)
    
    brand = relationship("Brand", back_populates="models")
    descriptions = relationship("Description", back_populates="model")
    vehicles = relationship("Vehicle", back_populates="model")
    
 