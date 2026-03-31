from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class AnswerBase(BaseModel):
    question_id: int
    correct_answer: str
    explanation: Optional[str] = None

class AnswerCreate(AnswerBase):
    pass

class AnswerResponse(AnswerBase):
    id: int
    
    class Config:
        from_attributes = True

class UserAnswerBase(BaseModel):
    question_id: int
    user_answer: str

class UserAnswerCreate(UserAnswerBase):
    pass

class UserAnswerResponse(UserAnswerBase):
    id: int
    user_id: int
    is_correct: bool
    score: float
    feedback: Optional[str] = None
    created_at: datetime
    
    class Config:
        from_attributes = True
