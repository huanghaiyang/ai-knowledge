from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from app.utils.database import Base

class Question(Base):
    __tablename__ = "questions"
    
    id = Column(Integer, primary_key=True, index=True)
    knowledge_id = Column(Integer, ForeignKey("knowledge_points.id"), nullable=False)
    question_type = Column(String(20), nullable=False)  # single_choice, multiple_choice, true_false, fill_blank, short_answer, code
    difficulty = Column(String(20), nullable=False)  # easy, medium, hard
    content = Column(Text, nullable=False)
    options = Column(Text)  # JSON格式存储选项
    correct_answer = Column(Text, nullable=False)
    explanation = Column(Text)
    
    # 关系
    knowledge = relationship("KnowledgePoint", back_populates="questions")
    answers = relationship("Answer", back_populates="question")
    user_answers = relationship("UserAnswer", back_populates="question")
