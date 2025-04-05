from pydantic import BaseModel
from typing import Optional

class DescriptionBase(BaseModel):
    name: str

class DescriptionCreate(DescriptionBase):
    pass

class DescriptionUpdate(DescriptionBase):
    pass

class DescriptionOut(DescriptionBase):
    id_description: int

    class Config:
        from_attributes = True 