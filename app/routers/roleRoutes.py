from fastapi import APIRouter, Depends, HTTPException, status, Body
from typing import List
from app.schemas.rolesSchema import RoleCreate, RoleOut
from app.services.roleService import RoleService
from app.repositories.roleRepository import RoleRepository
from app.database import get_db
from sqlalchemy.orm import Session

# Crear el router
router = APIRouter(
  prefix="/roles",
  tags=["roles"],
  responses={404: {"description": "Not found"}},
)

# Inyección de dependencias
def get_role_service(db: Session = Depends(get_db)):
    repo = RoleRepository(db)
    return RoleService(repo)

# Rutas
@router.post(
    "/",
    response_model=RoleOut,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new role",
    response_description="The created role"
)
async def create_role(
    role_data: RoleCreate = Body(..., example={"name": "admin"}),
    service: RoleService = Depends(get_role_service)
):
    """
    Create a new role with the following details:
    - **name**: The name of the role (must be unique)
    """
    return service.create_role(role_data)

@router.get(
    "/{role_id}",
    response_model=RoleOut,
    summary="Get a role by ID",
    responses={404: {"description": "Role not found"}}
)
async def get_role(
    role_id: int,
    service: RoleService = Depends(get_role_service)
):
    """
    Get details of a specific role by its ID.
    """
    role = service.get_role_by_id(role_id)
    if not role:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Role not found"
        )
    return role

@router.get(
    "/",
    response_model=List[RoleOut],
    summary="Get all roles"
)
async def list_roles(
    service: RoleService = Depends(get_role_service)
):
    """
    Retrieve a list of all available roles.
    """
    return service.get_all_roles()

@router.put(
    "/{role_id}",
    response_model=RoleOut,
    summary="Update a role",
    responses={
        200: {"description": "Role updated successfully"},
        404: {"description": "Role not found"}
    }
)
async def update_role(
    role_id: int,
    role_data: RoleCreate = Body(..., example={"name": "updated_name"}),
    service: RoleService = Depends(get_role_service)
):
    """
    Update an existing role's information.
    """
    updated_role = service.update_role(role_id, role_data)
    if not updated_role:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Role not found"
        )
    return updated_role

@router.delete(
    "/{role_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a role",
    responses={
        204: {"description": "Role deleted successfully"},
        404: {"description": "Role not found"}
    }
)
async def delete_role(
    role_id: int,
    service: RoleService = Depends(get_role_service)
):
    """
    Delete a specific role by its ID.
    """
    success = service.delete_role(role_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Role not found"
        )
    return None