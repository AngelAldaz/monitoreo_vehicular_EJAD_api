from pydantic import BaseModel, EmailStr
from typing import Optional

class UserBase(BaseModel):
  first_name: str
  last_name: str
  email: EmailStr

class UserCreate(UserBase):
  password: str

class UserOut(UserBase):
  id_usuario: int
  id_role_fk: int
  id_vehicle_fk: Optional[int] = None

  class Config:
    from_attributes = True

class UserLogin(BaseModel):
  email: EmailStr
  password: str
  
class Token(BaseModel):
    access_token: str

class TokenData(BaseModel):
    email: str | None = None