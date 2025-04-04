from pydantic import BaseModel

class RoleBase(BaseModel):
  name: str

class RoleCreate(RoleBase):
  pass

class RoleOut(RoleBase):
  id_role: int

  class Config:
    from_attributes = True