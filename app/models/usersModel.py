from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class User(Base):
  __tablename__ = "User"

  id_usuario = Column(Integer, primary_key=True, index=True, autoincrement=True)
  first_name = Column(String(50), nullable=False)
  last_name = Column(String(50), nullable=False)
  email = Column(String(100), nullable=False, unique=True)
  password = Column(String(255), nullable=False)
  id_role_fk = Column(Integer, ForeignKey("Role.id_role"), nullable=False)
  
  routes = relationship("Route", back_populates="user")