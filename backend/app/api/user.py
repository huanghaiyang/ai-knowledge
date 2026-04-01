from flask import request, jsonify
from sqlalchemy.orm import Session
from app.models.user import User
from app.utils.database import get_db
from app.utils.security import create_access_token, verify_password, get_current_user
from app.utils.validators import (
    validate_user_registration,
    record_registration,
    UserValidator
)

async def register(data: dict, client_ip: str, db: Session):
    # 清理用户输入，防止XSS
    username = UserValidator.sanitize_input(data.get('username', ''))
    email = data.get('email', '').lower().strip()  # 邮箱转小写并去除首尾空格
    password = data.get('password', '')
    
    # 执行完整的安全校验
    validate_user_registration(
        username=username,
        email=email,
        password=password,
        ip_address=client_ip
    )
    
    # 检查用户是否已存在（邮箱）
    db_user = db.query(User).filter(User.email == email).first()
    if db_user:
        return jsonify({"detail": "该邮箱已被注册"}), 400
    
    # 检查用户名是否已存在
    db_user_by_name = db.query(User).filter(User.username == username).first()
    if db_user_by_name:
        return jsonify({"detail": "该用户名已被使用"}), 400
    
    # 记录注册信息（用于频率限制）
    record_registration(client_ip, email)
    
    # 创建新用户
    new_user = User(
        username=username,
        email=email,
        password=password
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return jsonify({
        "id": new_user.id,
        "username": new_user.username,
        "email": new_user.email
    })

async def login(data: dict, db: Session):
    # 查找用户
    email = data.get('email', '')
    password = data.get('password', '')
    db_user = db.query(User).filter(User.email == email).first()
    if not db_user or not verify_password(password, db_user.password):
        return jsonify({"detail": "邮箱或密码错误"}), 401
    # 创建访问令牌
    access_token = create_access_token(data={"sub": db_user.email})
    return jsonify({"access_token": access_token, "token_type": "bearer"})

async def get_current_user_info(current_user: User):
    return jsonify({
        "id": current_user.id,
        "username": current_user.username,
        "email": current_user.email
    })

async def update_user_info(data: dict, current_user: User, db: Session):
    if 'username' in data:
        current_user.username = data['username']
    if 'difficulty_preference' in data:
        current_user.difficulty_preference = data['difficulty_preference']
    if 'knowledge_preference' in data:
        current_user.knowledge_preference = data['knowledge_preference']
    db.commit()
    db.refresh(current_user)
    return jsonify({
        "id": current_user.id,
        "username": current_user.username,
        "email": current_user.email
    })

def register_routes(app):
    @app.route('/api/user/register', methods=['POST'])
    async def flask_register():
        data = request.get_json()
        client_ip = request.remote_addr
        db = next(get_db())
        return await register(data, client_ip, db)
    
    @app.route('/api/user/login', methods=['POST'])
    async def flask_login():
        data = request.get_json()
        db = next(get_db())
        return await login(data, db)
    
    @app.route('/api/user/me', methods=['GET'])
    async def flask_get_current_user_info():
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({"detail": "未授权"}), 401
        token = token.split(' ')[1]
        current_user = get_current_user(token)
        if not current_user:
            return jsonify({"detail": "未授权"}), 401
        return await get_current_user_info(current_user)
    
    @app.route('/api/user/me', methods=['PUT'])
    async def flask_update_user_info():
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({"detail": "未授权"}), 401
        token = token.split(' ')[1]
        current_user = get_current_user(token)
        if not current_user:
            return jsonify({"detail": "未授权"}), 401
        data = request.get_json()
        db = next(get_db())
        return await update_user_info(data, current_user, db)
