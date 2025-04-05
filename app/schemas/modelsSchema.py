from pydantic import BaseModel
from typing import Optional
from app.schemas.brandsSchema import BrandOut

class ModelBase(BaseModel):
    name: str
    id_brand_fk: int

class ModelCreate(ModelBase):
    pass

class ModelUpdate(ModelBase):
    pass

class ModelOut(ModelBase):
    id_model: int
    name_brand: Optional[str] = None

    class Config:
        from_attributes = True

# Este esquema se usará cuando necesitemos incluir los detalles de la marca
class ModelWithBrand(ModelOut):
    brand: BrandOut

    class Config:
        from_attributes = True 