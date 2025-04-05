from sqlalchemy.orm import Session
from app.models.brandsModel import Brand

class BrandRepository:
  def __init__(self, db: Session) -> None:
    self.db = db
    
    
    
  def create_brand(self, brand: Brand) -> Brand:
      self.db.add(brand)
      self.db.commit()
      self.db.refresh(brand)
      return brand

  def get_brand_by_id(self, brand_id: int) -> Brand:
     result = self.db.query(Brand).filter(Brand.id_brand == brand_id)
     return result.first()
  
  def get_all_brands(self) -> list[Brand]:
     return self.db.query(Brand).all()

  def update_brand(self, brand: Brand) -> Brand:
     self.db.merge(brand)
     self.db.commit()
     self.db.refresh(brand)
     return brand
  
  def delete_brand(self, brand: Brand) -> bool:
     self.db.delete(brand)
     self.db.commit()
     return True
    
    
    
    
