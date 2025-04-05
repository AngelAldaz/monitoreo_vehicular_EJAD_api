from pydantic import BaseModel
from typing import Optional

class DescriptionBase(BaseModel):
    name: str
    id_model_fk: int

class DescriptionCreate(DescriptionBase):
    pass

class DescriptionUpdate(DescriptionBase):
    pass

class DescriptionOut(DescriptionBase):
    id_description: int
    name_model: Optional[str] = None

    class Config:
        from_attributes = True 