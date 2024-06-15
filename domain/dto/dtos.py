from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field

# TODO: Haviam objetos duplicados


class TarefaDTO(BaseModel):
    id: int
    title: str
    description: str
    status: str
    created_at: datetime = Field(default_factory=datetime.now)

    class Config:
        from_attributes = True


class TarefaCreateDTO(BaseModel):
    title: str
    description: str
    status: str

    class Config:
        from_attributes = True


class TarefaUpdateDTO(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None

    class Config:
        from_attributes = True
