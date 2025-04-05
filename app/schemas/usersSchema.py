from pydantic import BaseModel, EmailStr
from typing import Optional

class UserBase(BaseModel):
  first_name: str
  last_name: str
  email: EmailStr
  id_role_fk: int

class UserCreate(UserBase):
  password: str

class UserOut(UserBase):
  id_usuario: int

  class Config:
    from_attributes = True

class UserLogin(BaseModel):
  email: EmailStr
  password: str
  
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: str | None = None