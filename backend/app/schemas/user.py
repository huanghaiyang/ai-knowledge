from pydantic import BaseModel, EmailStr, Field, validator
from datetime import datetime
from typing import Optional
import re

class UserBase(BaseModel):
    username: str
    email: EmailStr

class UserCreate(UserBase):
    password: str = Field(..., description="用户密码")
    
    @validator('username')
    def validate_username(cls, v):
        """验证用户名格式"""
        if not v or len(v.strip()) < 3:
            raise ValueError('用户名长度不能少于3个字符')
        if len(v) > 20:
            raise ValueError('用户名长度不能超过20个字符')
        if v[0].isdigit():
            raise ValueError('用户名不能以数字开头')
        if not re.match(r'^[a-zA-Z0-9_\u4e00-\u9fa5]+$', v):
            raise ValueError('用户名只能包含字母、数字、下划线和中文')
        # 检查保留关键字
        reserved = {'admin', 'administrator', 'root', 'system', 'test', 'guest',
                   'user', 'manager', 'support', 'service', 'api', 'web'}
        if v.lower() in reserved:
            raise ValueError('该用户名已被保留，不能使用')
        return v.strip()
    
    @validator('password')
    def validate_password(cls, v):
        """验证密码强度"""
        if not v:
            raise ValueError('密码不能为空')
        if len(v) < 8:
            raise ValueError('密码长度不能少于8个字符')
        if len(v) > 128:
            raise ValueError('密码长度不能超过128个字符')
        if ' ' in v:
            raise ValueError('密码不能包含空格')
        if not re.search(r'[A-Z]', v):
            raise ValueError('密码必须包含至少一个大写字母')
        if not re.search(r'[a-z]', v):
            raise ValueError('密码必须包含至少一个小写字母')
        if not re.search(r'\d', v):
            raise ValueError('密码必须包含至少一个数字')
        if not re.search(r'[!@#$%^&*()_+\-=\[\]{};:\'",.<>?/\\|`~]', v):
            raise ValueError('密码必须包含至少一个特殊字符')
        return v
    
    @validator('email')
    def validate_email(cls, v):
        """验证邮箱格式并转小写"""
        if not v:
            raise ValueError('邮箱不能为空')
        # 检查禁止的邮箱域名
        blocked_domains = {'tempmail.com', '10minutemail.com', 'guerrillamail.com',
                          'mailinator.com', 'yopmail.com', 'throwawaymail.com'}
        try:
            domain = v.split('@')[1].lower()
            if domain in blocked_domains:
                raise ValueError('该邮箱域名不允许注册')
        except IndexError:
            raise ValueError('邮箱格式不正确')
        return v.lower().strip()

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserUpdate(BaseModel):
    username: Optional[str] = None
    difficulty_preference: Optional[str] = None
    knowledge_preference: Optional[str] = None

class UserResponse(UserBase):
    id: int
    created_at: datetime
    total_questions: int
    correct_questions: int
    learning_hours: int
    difficulty_preference: str
    knowledge_preference: str
    
    class Config:
        from_attributes = True
