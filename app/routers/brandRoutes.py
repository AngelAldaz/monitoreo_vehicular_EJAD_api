from fastapi import APIRouter, Depends, HTTPException, status, Body
from typing import List
from app.schemas.brandsSchema import BrandCreate, BrandOut
from app.services.brandService import BrandService
from app.repositories.brandRepository import BrandRepository
from app.database import get_db
from sqlalchemy.orm import Session

router = APIRouter(
  prefix="/brands",
  tags=["brands"],
  responses={404: {"description": "Not found"}},
)


def get_brand_service(db: Session = Depends(get_db)):
    repo = BrandRepository(db)
    return BrandService(repo)

@router.post(
    "/",
    response_model=BrandOut,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new brand",
    response_description="The created brand"
)   
async def create_brand(
    brand_data: BrandCreate = Body(..., example={"name": "Toyota"}),
    service: BrandService = Depends(get_brand_service)
):
    return service.create_brand(brand_data)

@router.get(
    "/{brand_id}",
    response_model=BrandOut,
    summary="Get a brand by ID",
    responses={404: {"description": "Brand not found"}}
)
async def get_brand(
    brand_id: int,
    service: BrandService = Depends(get_brand_service)
):
    brand = service.get_brand_by_id(brand_id)
    if not brand:
        raise HTTPException(status_code=404, detail="Brand not found")
    return brand

@router.get(
    "/",
    response_model=List[BrandOut],
    summary="Get all brands"
)
async def list_brands(
    service: BrandService = Depends(get_brand_service)
):
    return service.get_all_brands()

@router.put(
    "/{brand_id}",
    response_model=BrandOut,
    summary="Update a brand",
    responses={
        200: {"description": "Brand updated successfully"},
        404: {"description": "Brand not found"}
    }
)
async def update_brand(
    brand_id: int,
    brand_data: BrandCreate = Body(..., example={"name": "Updated Brand"}),
    service: BrandService = Depends(get_brand_service)
):
    updated_brand = service.update_brand(brand_id, brand_data)
    if not updated_brand:
        raise HTTPException(status_code=404, detail="Brand not found")
    return updated_brand

@router.delete(
    "/{brand_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a brand",
    responses={
        204: {"description": "Brand deleted successfully"},
        404: {"description": "Brand not found"}
    }
)
async def delete_brand(
    brand_id: int,
    service: BrandService = Depends(get_brand_service)
):
    success = service.delete_brand(brand_id)
    if not success:
        raise HTTPException(status_code=404, detail="Brand not found")
    return None



