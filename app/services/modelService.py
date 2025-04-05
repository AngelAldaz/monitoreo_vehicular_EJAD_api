from typing import Optional
from app.schemas.modelsSchema import ModelCreate, ModelOut
from app.repositories.modelRepository import ModelRepository
from app.models.modelsModel import Model

class ModelService:
  def __init__(self, model_repo: ModelRepository) -> None:
    self.repo = model_repo
    
  def create_model(self, model: ModelCreate) -> ModelOut:
    db_model = Model(name=model.name, id_brand_fk=model.id_brand_fk)
    created_model = self.repo.create_model(db_model)
    return ModelOut(
      id_model=created_model.id_model, 
      name=created_model.name, 
      id_brand_fk=created_model.id_brand_fk,
      name_brand=created_model.brand.name if created_model.brand else None
    )
  
  def get_model_by_id(self, model_id: int) -> Optional[ModelOut]:
    db_model = self.repo.get_model_by_id(model_id)
    if db_model is not None:
      return ModelOut(
        id_model=db_model.id_model, 
        name=db_model.name, 
        id_brand_fk=db_model.id_brand_fk,
        name_brand=db_model.brand.name if db_model.brand else None
      )
    return None
  
  def get_all_models(self) -> list[ModelOut]:
    db_models = self.repo.get_all_models()
    return [
      ModelOut(
        id_model=model.id_model, 
        name=model.name, 
        id_brand_fk=model.id_brand_fk,
        name_brand=model.brand.name if model.brand else None
      ) for model in db_models
    ]
  
  def update_model(self, id_model: int, model: ModelCreate) -> Optional[ModelOut]:
    db_model = self.repo.get_model_by_id(id_model)
    if db_model is not None:
      db_model.name = model.name
      db_model.id_brand_fk = model.id_brand_fk
      updated_model = self.repo.update_model(db_model)
      return ModelOut(
        id_model=updated_model.id_model, 
        name=updated_model.name, 
        id_brand_fk=updated_model.id_brand_fk,
        name_brand=updated_model.brand.name if updated_model.brand else None
      )
    return None

  def delete_model(self, id_model: int) -> bool:
    db_model = self.repo.get_model_by_id(id_model)
    if db_model is not None:
      return self.repo.delete_model(db_model)
    return False


