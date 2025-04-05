from sqlalchemy.orm import Session
from app.models.MaintenanceModel import Maintenance
from typing import List

class MaintenanceRepository:
  def __init__(self, db: Session) -> None:
    self.db = db
      
  def create_maintenance(self, maintenance: Maintenance) -> Maintenance:
    self.db.add(maintenance)
    self.db.commit()
    self.db.refresh(maintenance)
    return maintenance
  
  def get_maintenance_by_id(self, maintenance_id: int) -> Maintenance:
    return self.db.query(Maintenance).filter(Maintenance.id_maintenance == maintenance_id).first()
  
  def get_all_maintenances(self) -> List[Maintenance]:
    return self.db.query(Maintenance).all()
  
  def update_maintenance(self, maintenance: Maintenance) -> Maintenance:
    self.db.merge(maintenance)
    self.db.commit()
    self.db.refresh(maintenance)
    return maintenance
  
  def delete_maintenance(self, maintenance: Maintenance) -> bool:
    self.db.delete(maintenance)
    self.db.commit()
    return True
  
  def get_maintenances_by_status(self, status: str) -> List[Maintenance]:
    return self.db.query(Maintenance).filter(Maintenance.status == status).all()