from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.database import Base

class Brand(Base):
    __tablename__ = "Brand"

    id_brand = Column(Integer, primary_key=True, index=True, autoincrement=True)
    
    name = Column(String(50), nullable=False)
    
    
    models = relationship("Model", back_populates="brand")
