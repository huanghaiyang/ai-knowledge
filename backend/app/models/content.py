from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from app.utils.database import Base

class KnowledgeContent(Base):
    __tablename__ = "knowledge_content"
    
    id = Column(Integer, primary_key=True, index=True)
    knowledge_id = Column(Integer, ForeignKey("knowledge_points.id"), nullable=False)
    section_title = Column(String(200), nullable=False)
    content = Column(Text, nullable=False)
    order = Column(Integer, nullable=False)  # 章节顺序
    
    # 关系
    knowledge = relationship("KnowledgePoint", backref="content")
