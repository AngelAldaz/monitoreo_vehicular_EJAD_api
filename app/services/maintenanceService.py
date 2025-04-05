from typing import List, Optional
from app.schemas.maintenanceSchema import MaintenanceCreate, MaintenanceOut, MaintenanceUpdate
from app.repositories.maintenanceRepository import MaintenanceRepository
from app.models.MaintenanceModel import Maintenance

class MaintenanceService:
  def __init__(self, maintenance_repo: MaintenanceRepository) -> None:
    self.repo = maintenance_repo
      
  def create_maintenance(self, maintenance: MaintenanceCreate) -> MaintenanceOut:
    db_maintenance = Maintenance(
      # id_vehicle_fk=maintenance.id_vehicle_fk,
      description=maintenance.description,
      start_time=maintenance.start_time,
      estimated_time=maintenance.estimated_time,
      end_time=maintenance.end_time,
      status=maintenance.status
    )
    created_maintenance = self.repo.create_maintenance(db_maintenance)
    return MaintenanceOut(
      id_maintenance=created_maintenance.id_maintenance,
      # id_vehicle_fk=created_maintenance.id_vehicle_fk,
      description=created_maintenance.description,
      start_time=created_maintenance.start_time,
      estimated_time=created_maintenance.estimated_time,
      end_time=created_maintenance.end_time,
      status=created_maintenance.status
    )
  
  def get_maintenance_by_id(self, maintenance_id: int) -> Optional[MaintenanceOut]:
    db_maintenance = self.repo.get_maintenance_by_id(maintenance_id)
    if db_maintenance:
      return MaintenanceOut(
        id_maintenance=db_maintenance.id_maintenance,
        # id_vehicle_fk=db_maintenance.id_vehicle_fk,
        description=db_maintenance.description,
        start_time=db_maintenance.start_time,
        estimated_time=db_maintenance.estimated_time,
        end_time=db_maintenance.end_time,
        status=db_maintenance.status
      )
  
  def get_all_maintenances(self) -> List[MaintenanceOut]:
    db_maintenances = self.repo.get_all_maintenances()
    return [
      MaintenanceOut(
        id_maintenance=m.id_maintenance,
        # id_vehicle_fk=m.id_vehicle_fk,
        description=m.description,
        start_time=m.start_time,
        estimated_time=m.estimated_time,
        end_time=m.end_time,
        status=m.status
      ) for m in db_maintenances
    ]
  
  def update_maintenance(self, maintenance_id: int, maintenance: MaintenanceUpdate) -> Optional[MaintenanceOut]:
    db_maintenance = self.repo.get_maintenance_by_id(maintenance_id)
    if db_maintenance:
      if maintenance.description is not None:
        db_maintenance.description = maintenance.description
      if maintenance.estimated_time is not None:
        db_maintenance.estimated_time = maintenance.estimated_time
      if maintenance.end_time is not None:
        db_maintenance.end_time = maintenance.end_time
      if maintenance.status is not None:
        db_maintenance.status = maintenance.status
          
      updated_maintenance = self.repo.update_maintenance(db_maintenance)
      return MaintenanceOut(
        id_maintenance=updated_maintenance.id_maintenance,
        # id_vehicle_fk=updated_maintenance.id_vehicle_fk,
        description=updated_maintenance.description,
        start_time=updated_maintenance.start_time,
        estimated_time=updated_maintenance.estimated_time,
        end_time=updated_maintenance.end_time,
        status=updated_maintenance.status
      )
  
  def delete_maintenance(self, maintenance_id: int) -> bool:
    db_maintenance = self.repo.get_maintenance_by_id(maintenance_id)
    if db_maintenance:
      return self.repo.delete_maintenance(db_maintenance)
    return False
  
  def get_maintenances_by_status(self, status: str) -> List[MaintenanceOut]:
    db_maintenances = self.repo.get_maintenances_by_status(status)
    return [
      MaintenanceOut(
        id_maintenance=m.id_maintenance,
        # id_vehicle_fk=m.id_vehicle_fk,
        description=m.description,
        start_time=m.start_time,
        estimated_time=m.estimated_time,
        end_time=m.end_time,
        status=m.status
      ) for m in db_maintenances
    ]