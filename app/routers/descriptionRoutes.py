from fastapi import APIRouter, Depends, HTTPException, status, Body
from typing import List
import app.schemas.descriptionsSchema as descriptionsSchema
import app.services.descriptionService as descriptionService
import app.repositories.descriptionRepository as descriptionRepository
from app.database import get_db
from sqlalchemy.orm import Session

router = APIRouter(
  prefix="/descriptions",
  tags=["descriptions"],
  responses={404: {"description": "Not found"}},
)

def get_description_service(db: Session = Depends(get_db)):
    repo = descriptionRepository.DescriptionRepository(db)
    return descriptionService.DescriptionService(repo)

@router.post(
    "/",
    response_model=descriptionsSchema.DescriptionOut,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new description",
    response_description="The created description"
)   
async def create_description(
    description_data: descriptionsSchema.DescriptionCreate = Body(..., example={"name": "Toyota", "id_model_fk": 1}),
    service: descriptionService.DescriptionService = Depends(get_description_service)
):
    return service.create_description(description_data)

@router.get(
    "/{description_id}",
    response_model=descriptionsSchema.DescriptionOut,
    summary="Get a description by ID",
    responses={404: {"description": "Description not found"}}
)
async def get_description(
    description_id: int,
    service: descriptionService.DescriptionService = Depends(get_description_service)
):
    description = service.get_description_by_id(description_id)
    if not description:
        raise HTTPException(status_code=404, detail="Description not found")
    return description

@router.get(
    "/",
    response_model=List[descriptionsSchema.DescriptionOut],
    summary="Get all descriptions"
)
async def list_descriptions(
    service: descriptionService.DescriptionService = Depends(get_description_service)
):
    return service.get_all_descriptions()

@router.put(
    "/{description_id}",
    response_model=descriptionsSchema.DescriptionOut,
    summary="Update a description",
    responses={
        200: {"description": "Description updated successfully"},
        404: {"description": "Description not found"}
    }
)   
async def update_description(
    description_id: int,
    description_data: descriptionsSchema.DescriptionCreate = Body(..., example={"name": "Updated Description", "id_model_fk": 1}),
    service: descriptionService.DescriptionService = Depends(get_description_service)
):
    updated_description = service.update_description(description_id, description_data)
    if not updated_description:
        raise HTTPException(status_code=404, detail="Description not found")
    return updated_description

@router.delete(
    "/{description_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a description",
    responses={
        204: {"description": "Description deleted successfully"},
        404: {"description": "Description not found"}
    }
)
async def delete_description(
    description_id: int,
    service: descriptionService.DescriptionService = Depends(get_description_service)
):
    success = service.delete_description(description_id)
    if not success:
        raise HTTPException(status_code=404, detail="Description not found")
    return None


