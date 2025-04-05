from pydantic import BaseModel
from typing import List, Optional

# Esquema base con los campos comunes para Brand
class BrandBase(BaseModel):
    name: str  # Campo obligatorio para el nombre de la marca

# Esquema para crear una nueva marca (sin ID porque será generado por la base de datos)
class BrandCreate(BrandBase):
    pass

# Esquema para actualizar una marca existente
class BrandUpdate(BrandBase):
    pass 

# Esquema para devolver una marca con su ID (respuesta de la API)
class BrandOut(BrandBase):
    id_brand: int  # Incluye el ID generado por la base de datos

    class Config:
        from_attributes = True  # Permite la conversión automática de objetos ORM a este esquema

# Esquema que extiende BrandOut para incluir los modelos relacionados a esta marca
class BrandWithModels(BrandOut):
    models: List["ModelOut"] = []  # Lista de modelos que pertenecen a esta marca

    class Config:
        from_attributes = True  # Permite cargar relaciones desde el ORM

# Importación al final para evitar referencia circular entre schemas
from app.schemas.modelsSchema import ModelOut 