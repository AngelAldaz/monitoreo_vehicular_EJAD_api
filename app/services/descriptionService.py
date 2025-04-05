from typing import Optional
from app.schemas.descriptionsSchema import DescriptionCreate, DescriptionOut
from app.repositories.descriptionRepository import DescriptionRepository
from app.models.descriptionsModel import Description

class DescriptionService:
  def __init__(self, description_repo: DescriptionRepository) -> None:
    self.repo = description_repo
    
  def create_description(self, description: DescriptionCreate) -> DescriptionOut:
    db_description = Description(name=description.name, id_model_fk=description.id_model_fk)
    created_description = self.repo.create_description(db_description)
    return DescriptionOut(
      id_description=created_description.id_description,
      name=created_description.name,
      id_model_fk=created_description.id_model_fk,
      name_model=created_description.model.name if created_description.model else None
    )
  
  def get_description_by_id(self, description_id: int) -> Optional[DescriptionOut]:
    db_description = self.repo.get_description_by_id(description_id)
    if db_description is not None:
      return DescriptionOut(
        id_description=db_description.id_description,
        name=db_description.name,
        id_model_fk=db_description.id_model_fk,
        name_model=db_description.model.name if db_description.model else None
      )
    return None
  
  def get_descriptions_by_model_id(self, model_id: int) -> list[DescriptionOut]:
    db_descriptions = self.repo.get_descriptions_by_model_id(model_id)
    return [
      DescriptionOut(
        id_description=description.id_description,
        name=description.name,
        id_model_fk=description.id_model_fk,
        name_model=description.model.name if description.model else None
      ) for description in db_descriptions
    ]
  
  def get_all_descriptions(self) -> list[DescriptionOut]:
    db_descriptions = self.repo.get_all_descriptions()
    return [
      DescriptionOut(
        id_description=description.id_description,
        name=description.name,
        id_model_fk=description.id_model_fk,
        name_model=description.model.name if description.model else None
      ) for description in db_descriptions
    ]
  
  def update_description(self, id_description: int, description: DescriptionCreate) -> Optional[DescriptionOut]:
    db_description = self.repo.get_description_by_id(id_description)
    if db_description is not None:
      db_description.name = description.name
      db_description.id_model_fk = description.id_model_fk
      updated_description = self.repo.update_description(db_description)
      return DescriptionOut(
        id_description=updated_description.id_description,
        name=updated_description.name,
        id_model_fk=updated_description.id_model_fk,
        name_model=updated_description.model.name if updated_description.model else None
      )
    return None
  
  def delete_description(self, id_description: int) -> bool:
    db_description = self.repo.get_description_by_id(id_description)
    if db_description is not None:
      return self.repo.delete_description(db_description)
    return False
  
    
    

