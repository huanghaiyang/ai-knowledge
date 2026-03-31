from pydantic import BaseModel
from typing import Optional

class QuestionBase(BaseModel):
    knowledge_id: int
    question_type: str
    difficulty: str
    content: str
    options: Optional[str] = None
    correct_answer: str
    explanation: Optional[str] = None

class QuestionCreate(QuestionBase):
    pass

class QuestionUpdate(BaseModel):
    knowledge_id: Optional[int] = None
    question_type: Optional[str] = None
    difficulty: Optional[str] = None
    content: Optional[str] = None
    options: Optional[str] = None
    correct_answer: Optional[str] = None
    explanation: Optional[str] = None

class QuestionResponse(QuestionBase):
    id: int
    
    class Config:
        from_attributes = True
