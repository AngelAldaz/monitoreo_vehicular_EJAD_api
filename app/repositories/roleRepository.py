from sqlalchemy.orm import Session
from app.models.rolesModel import Role

class RoleRepository:
  def __init__(self, db: Session) -> None:
    self.db = db
    
  def create_role(self, role: Role) -> Role:
    self.db.add(role)
    self.db.commit()
    self.db.refresh(role)
    return role
  
  def get_role_by_id(self, role_id: int) -> Role:
    result = self.db.query(Role).filter(Role.id_role == role_id)
    return result.first()
  
  def get_all_roles(self) -> list[Role]:
    return self.db.query(Role).all()
  
  def update_role(self, role: Role) -> Role:
    self.db.merge(role)
    self.db.commit()
    self.db.refresh(role)
    return role
  
  def delete_role(self, role: Role) -> bool:
    self.db.delete(role)
    self.db.commit()
    return True