from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from flask import g
from app.utils.config import SECRET_KEY
from app.utils.database import get_db
from app.models.user import User
from app.utils.common import verify_password, get_password_hash

# 密钥
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def get_current_user(token: str):
    # 使用g对象来管理数据库会话
    if not hasattr(g, 'db'):
        g.db = next(get_db())
    db = g.db
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            return None
        # 验证令牌是否过期
        exp = payload.get("exp")
        if exp is None or datetime.utcnow() > datetime.fromtimestamp(exp):
            return None
    except JWTError:
        return None
    user = db.query(User).filter(User.email == email).first()
    if user is None:
        return None
    return user

def verify_token(token: str) -> dict:
    """
    验证令牌并返回载荷
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        # 验证令牌是否过期
        exp = payload.get("exp")
        if exp is None or datetime.utcnow() > datetime.fromtimestamp(exp):
            return {"valid": False, "error": "令牌已过期"}
        return {"valid": True, "payload": payload}
    except JWTError as e:
        return {"valid": False, "error": str(e)}

from functools import wraps
from flask import request, jsonify

def login_required(f):
    """
    认证装饰器，验证用户是否已登录
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({"detail": "未授权"}), 401
        token = token.split(' ')[1]
        current_user = get_current_user(token)
        if not current_user:
            return jsonify({"detail": "未授权"}), 401
        # 将当前用户添加到g对象中，以便在路由函数中使用
        g.current_user = current_user
        return f(*args, **kwargs)
    return decorated_function
