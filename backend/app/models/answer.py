from sqlalchemy import Column, Integer, String, Text, ForeignKey, Boolean, DateTime, Float
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.utils.database import Base

class Answer(Base):
    __tablename__ = "answers"
    
    id = Column(Integer, primary_key=True, index=True)
    question_id = Column(Integer, ForeignKey("questions.id"), nullable=False)
    correct_answer = Column(Text, nullable=False)
    explanation = Column(Text)
    
    # 关系
    question = relationship("Question", back_populates="answers")

class UserAnswer(Base):
    __tablename__ = "user_answers"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    question_id = Column(Integer, ForeignKey("questions.id"), nullable=False)
    user_answer = Column(Text, nullable=False)
    is_correct = Column(Boolean, nullable=False)
    score = Column(Float, nullable=False)
    feedback = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # 关系
    user = relationship("User")
    question = relationship("Question", back_populates="user_answers")
