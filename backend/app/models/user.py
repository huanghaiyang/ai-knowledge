from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.sql import func
from app.utils.database import Base
from app.utils.common import get_password_hash

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    _password = Column("password", String(100), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    is_active = Column(Boolean, default=True)
    
    # 密码属性
    @property
    def password(self):
        return self._password
    
    @password.setter
    def password(self, value):
        self._password = get_password_hash(value)
    
    # 学习统计相关字段
    total_questions = Column(Integer, default=0)
    correct_questions = Column(Integer, default=0)
    learning_hours = Column(Integer, default=0)
    
    # 学习偏好设置
    difficulty_preference = Column(String(20), default="medium")  # easy, medium, hard
    knowledge_preference = Column(String(100), default="")  # 逗号分隔的知识点ID
