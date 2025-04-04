from sqlalchemy import Column, Integer, String
from app.database import Base

class Role(Base):
    __tablename__ = "Role"

    id_role = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(50), nullable=False)