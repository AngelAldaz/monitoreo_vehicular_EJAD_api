from typing import Optional
from app.schemas.brandsSchema import BrandCreate, BrandOut
from app.repositories.brandRepository import BrandRepository
from app.models.brandsModel import Brand

class BrandService:
  def __init__(self, brand_repo: BrandRepository) -> None:
    self.repo = brand_repo
    
  def create_brand(self, brand: BrandCreate) -> BrandOut:
    db_brand = Brand(name=brand.name)
    created_brand = self.repo.create_brand(db_brand)
    return BrandOut(id_brand=created_brand.id_brand, name=created_brand.name)
  
  def get_brand_by_id(self, brand_id: int) -> Optional[BrandOut]:
    db_brand = self.repo.get_brand_by_id(brand_id)
    if db_brand is not None:
      return BrandOut(id_brand=db_brand.id_brand, name=db_brand.name)
    return None

  def get_all_brands(self) -> list[BrandOut]:
    db_brands = self.repo.get_all_brands()
    return [BrandOut(id_brand=brand.id_brand, name=brand.name) for brand in db_brands]
  
  def update_brand(self, id_brand: int, brand: BrandCreate) -> Optional[BrandOut]:
    db_brand = self.repo.get_brand_by_id(id_brand)
    if db_brand is not None:
      db_brand.name = brand.name
      updated_brand = self.repo.update_brand(db_brand)
      return BrandOut(id_brand=updated_brand.id_brand, name=updated_brand.name)
    return None

  def delete_brand(self, id_brand: int) -> bool:
    db_brand = self.repo.get_brand_by_id(id_brand)
    if db_brand is not None:
      return self.repo.delete_brand(db_brand)
    return False
    
