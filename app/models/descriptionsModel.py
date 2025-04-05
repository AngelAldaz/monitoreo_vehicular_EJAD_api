from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base


class Description(Base):
    __tablename__ = "Description"

    id_description = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    
    id_model_fk = Column(Integer, ForeignKey("Model.id_model"), nullable=False)
    
    model = relationship("Model", back_populates="descriptions")
    vehicles = relationship("Vehicle", back_populates="description")
