from fastapi import APIRouter, Depends, HTTPException, status, Body
from typing import List
import app.schemas.modelsSchema as modelsSchema
import app.services.modelService as modelService
import app.repositories.modelRepository as modelRepository
from app.database import get_db
from sqlalchemy.orm import Session


router = APIRouter(
  prefix="/models",
  tags=["models"],
  responses={404: {"description": "Not found"}},
)   

def get_model_service(db: Session = Depends(get_db)):
    repo = modelRepository.ModelRepository(db)
    return modelService.ModelService(repo)

@router.post(
    "/",
    response_model=modelsSchema.ModelOut,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new model",
    response_description="The created model"
)   
async def create_model(
    model_data: modelsSchema.ModelCreate = Body(..., example={"name": "Toyota", "id_brand_fk": 1}),
    service: modelService.ModelService = Depends(get_model_service)
):
    return service.create_model(model_data)

@router.get(
    "/{model_id}",
    response_model=modelsSchema.ModelOut,
    summary="Get a model by ID",
    responses={404: {"description": "Model not found"}}
)   
async def get_model(
    model_id: int,
    service: modelService.ModelService = Depends(get_model_service)
):
    model = service.get_model_by_id(model_id)
    if not model:   
        raise HTTPException(status_code=404, detail="Model not found")
    return model

@router.get(
    "/",
    response_model=List[modelsSchema.ModelOut], 
    summary="Get all models"
)
async def list_models(
    service: modelService.ModelService = Depends(get_model_service)
):
    return service.get_all_models() 

@router.put(
    "/{model_id}",
    response_model=modelsSchema.ModelOut,
    summary="Update a model",
    responses={
        200: {"description": "Model updated successfully"},
        404: {"description": "Model not found"}
    }
)
async def update_model(
    model_id: int,
    model_data: modelsSchema.ModelCreate = Body(..., example={"name": "Updated Model", "id_brand_fk": 1}),
    service: modelService.ModelService = Depends(get_model_service) 
):
    updated_model = service.update_model(model_id, model_data)
    if not updated_model:
        raise HTTPException(status_code=404, detail="Model not found")
    return updated_model   

@router.delete(
    "/{model_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a model",
    responses={
        204: {"description": "Model deleted successfully"},
        404: {"description": "Model not found"}
    }
)
async def delete_model(
    model_id: int,
    service: modelService.ModelService = Depends(get_model_service)
):
    success = service.delete_model(model_id)
    if not success:
        raise HTTPException(status_code=404, detail="Model not found")
    return None



