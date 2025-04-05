from sqlalchemy.orm import Session, joinedload
from app.models.descriptionsModel import Description
from app.models.modelsModel import Model

class DescriptionRepository:
  def __init__(self, db: Session) -> None:
    self.db = db    
    
  def create_description(self, description: Description) -> Description:
    self.db.add(description)
    self.db.commit()
    self.db.refresh(description)
    self.db.refresh(description, attribute_names=['model'])
    return description
  
  def get_description_by_id(self, description_id: int) -> Description:
    result = self.db.query(Description).options(joinedload(Description.model)).filter(Description.id_description == description_id)
    return result.first()

  def get_descriptions_by_model_id(self, description_id: int) -> list[Description]:
    return self.db.query(Description).options(joinedload(Description.model)).filter(Description.id_model_fk == description_id).all()
  
  def get_all_descriptions(self) -> list[Description]:
    return self.db.query(Description).options(joinedload(Description.model)).all()

  def update_description(self, description: Description) -> Description:
    self.db.merge(description)
    self.db.commit()
    self.db.refresh(description)
    
    self.db.refresh(description, attribute_names=['model'])
    return description

  def delete_description(self, description: Description) -> bool:
    self.db.delete(description)
    self.db.commit()
    return True
  
  
  
    
    
    

