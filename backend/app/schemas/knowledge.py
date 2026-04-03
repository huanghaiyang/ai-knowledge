from pydantic import BaseModel
from typing import Optional, List

class KnowledgePointBase(BaseModel):
    title: str
    description: Optional[str] = None
    parent_id: Optional[int] = None
    level: int
    order: int = 0

class KnowledgePointCreate(KnowledgePointBase):
    pass

class KnowledgePointUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    parent_id: Optional[int] = None
    level: Optional[int] = None
    order: Optional[int] = None

class KnowledgePointResponse(KnowledgePointBase):
    id: int
    
    class Config:
        from_attributes = True
