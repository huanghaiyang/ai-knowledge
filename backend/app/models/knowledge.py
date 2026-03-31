from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from app.utils.database import Base

class KnowledgePoint(Base):
    __tablename__ = "knowledge_points"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100), nullable=False)
    description = Column(Text)
    parent_id = Column(Integer, ForeignKey("knowledge_points.id"), nullable=True)
    level = Column(Integer, nullable=False)  # 1: 一级知识点, 2: 二级知识点, 3: 三级知识点
    
    # 关系
    parent = relationship("KnowledgePoint", remote_side=[id], backref="children")
    questions = relationship("Question", back_populates="knowledge")
