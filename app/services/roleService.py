from typing import Optional
from app.schemas.rolesSchema import RoleCreate, RoleOut
from app.repositories.roleRepository import RoleRepository
from app.models.rolesModel import Role

class RoleService:
  def __init__(self, role_repo: RoleRepository) -> None:
    self.repo = role_repo
    
  def create_role(self, role: RoleCreate) -> RoleOut:
    db_role = Role(name=role.name)
    created_role = self.repo.create_role(db_role)
    return RoleOut(id_role=created_role.id_role, name=created_role.name)
  
  def get_role_by_id(self, role_id: int) -> Optional[RoleOut]:
    db_role = self.repo.get_role_by_id(role_id)
    if db_role is not None:
      return RoleOut(id_role=db_role.id_role, name=db_role.name)
  
  def get_all_roles(self) -> list[RoleOut]:
    db_roles = self.repo.get_all_roles()
    return [RoleOut(id_role=role.id_role, name=role.name) for role in db_roles]
  
  def update_role(self, id_role: int, role: RoleCreate) -> Optional[RoleOut]:
    db_role = self.repo.get_role_by_id(id_role)
    if db_role is not None:
      db_role.name = role.name
      updated_role = self.repo.update_role(db_role)
      return RoleOut(id_role=updated_role.id_role, name=updated_role.name)
    
  def delete_role(self, id_role: int) -> bool:
    db_role = self.repo.get_role_by_id(id_role)
    if db_role is not None:
      return self.repo.delete_role(db_role)