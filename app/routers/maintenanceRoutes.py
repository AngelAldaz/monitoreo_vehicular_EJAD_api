from fastapi import APIRouter, Depends, HTTPException, status, Body
from typing import List
from sqlalchemy.orm import Session
from app.schemas.maintenanceSchema import (
  MaintenanceCreate,
  MaintenanceOut,
  MaintenanceUpdate,
  MaintenanceStatus
)
from app.services.maintenanceService import MaintenanceService
from app.repositories.maintenanceRepository import MaintenanceRepository
from app.database import get_db

router = APIRouter(
  prefix="/maintenances",
  tags=["maintenances"],
  responses={404: {"description": "Not found"}},
)

def get_maintenance_service(db: Session = Depends(get_db)):
  repo = MaintenanceRepository(db)
  return MaintenanceService(repo)

@router.post(
  "/",
  response_model=MaintenanceOut,
  status_code=status.HTTP_201_CREATED,
  summary="Create a new maintenance",
  response_description="The created maintenance"
)
async def create_maintenance(
  maintenance_data: MaintenanceCreate = Body(...),
  service: MaintenanceService = Depends(get_maintenance_service)
):
  """
  Create a new maintenance record with the following details:
  - **start_time**: When the maintenance starts
  - **estimated_time**: Estimated duration of the maintenance
  - **status**: Current status of the maintenance
  - **description**: (Optional) Description of the maintenance
  - **end_time**: (Optional) When the maintenance ended
  """
  return service.create_maintenance(maintenance_data)

@router.get(
  "/{maintenance_id}",
  response_model=MaintenanceOut,
  summary="Get a maintenance by ID",
  responses={404: {"description": "Maintenance not found"}}
)
async def get_maintenance(
  maintenance_id: int,
  service: MaintenanceService = Depends(get_maintenance_service)
):
  """
  Get details of a specific maintenance by its ID.
  """
  maintenance = service.get_maintenance_by_id(maintenance_id)
  if not maintenance:
    raise HTTPException(
      status_code=status.HTTP_404_NOT_FOUND,
      detail="Maintenance not found"
    )
  return maintenance

@router.get(
  "/",
  response_model=List[MaintenanceOut],
  summary="Get all maintenances"
)
async def list_maintenances(
  service: MaintenanceService = Depends(get_maintenance_service)
):
  """
  Retrieve a list of all maintenance records.
  """
  return service.get_all_maintenances()

@router.get(
  "/status/{status}",
  response_model=List[MaintenanceOut],
  summary="Get maintenances by status"
)
async def list_maintenances_by_status(
  status: MaintenanceStatus,
  service: MaintenanceService = Depends(get_maintenance_service)
):
  """
  Retrieve maintenance records filtered by status.
  """
  return service.get_maintenances_by_status(status)

@router.put(
  "/{maintenance_id}",
  response_model=MaintenanceOut,
  summary="Update a maintenance",
  responses={
    200: {"description": "Maintenance updated successfully"},
    404: {"description": "Maintenance not found"}
  }
)
async def update_maintenance(
  maintenance_id: int,
  maintenance_data: MaintenanceUpdate = Body(...),
  service: MaintenanceService = Depends(get_maintenance_service)
):
  """
  Update an existing maintenance's information.
  """
  updated_maintenance = service.update_maintenance(maintenance_id, maintenance_data)
  if not updated_maintenance:
    raise HTTPException(
      status_code=status.HTTP_404_NOT_FOUND,
      detail="Maintenance not found"
    )
  return updated_maintenance

@router.delete(
  "/{maintenance_id}",
  status_code=status.HTTP_204_NO_CONTENT,
  summary="Delete a maintenance",
  responses={
    204: {"description": "Maintenance deleted successfully"},
    404: {"description": "Maintenance not found"}
  }
)
async def delete_maintenance(
  maintenance_id: int,
  service: MaintenanceService = Depends(get_maintenance_service)
):
  """
  Delete a specific maintenance by its ID.
  """
  success = service.delete_maintenance(maintenance_id)
  if not success:
    raise HTTPException(
      status_code=status.HTTP_404_NOT_FOUND,
      detail="Maintenance not found"
    )
  return None