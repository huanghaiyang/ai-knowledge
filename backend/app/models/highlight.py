from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from app.utils.database import Base

class KnowledgeHighlight(Base):
    __tablename__ = "knowledge_highlights"
    
    id = Column(Integer, primary_key=True, index=True)
    knowledge_id = Column(Integer, ForeignKey("knowledge_points.id"), nullable=False)
    section_id = Column(Integer, ForeignKey("knowledge_content.id"), nullable=True)
    highlight_id = Column(String(100), nullable=False, unique=True)
    text = Column(Text, nullable=False)
    note = Column(Text, nullable=True)
    start_pos = Column(Integer, nullable=False)
    end_pos = Column(Integer, nullable=False)
    start_context = Column(Text, nullable=True)
    end_context = Column(Text, nullable=True)
    created_at = Column(Integer, nullable=False)
    
    knowledge = relationship("KnowledgePoint", backref="highlights")
    section = relationship("KnowledgeContent", backref="highlights")
