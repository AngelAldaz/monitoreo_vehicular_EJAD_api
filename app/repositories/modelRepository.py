from sqlalchemy.orm import Session, joinedload
from app.models.modelsModel import Model
from app.models.brandsModel import Brand

class ModelRepository:
  def __init__(self, db: Session) -> None:
    self.db = db
    
  def create_model(self, model: Model) -> Model:
    self.db.add(model)
    self.db.commit()
    self.db.refresh(model)
    
    self.db.refresh(model, attribute_names=['brand'])
    return model
  
  def get_model_by_id(self, model_id: int) -> Model:
    result = self.db.query(Model).options(joinedload(Model.brand)).filter(Model.id_model == model_id)
    return result.first()
  
  def get_all_models(self) -> list[Model]:
    return self.db.query(Model).options(joinedload(Model.brand)).all()
  
  def update_model(self, model: Model) -> Model:
    self.db.merge(model)
    self.db.commit()
    self.db.refresh(model)
    # Carga explícita de la relación brand
    self.db.refresh(model, attribute_names=['brand'])
    return model

  def delete_model(self, model: Model) -> bool:
    self.db.delete(model)
    self.db.commit()
    return True