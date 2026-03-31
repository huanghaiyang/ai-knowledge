from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user import UserCreate, UserLogin, UserResponse, UserUpdate
from app.utils.database import get_db
from app.utils.security import create_access_token, verify_password, get_current_user
from app.utils.validators import (
    validate_user_registration,
    record_registration,
    UserValidator
)

router = APIRouter()

@router.post("/register", response_model=UserResponse)
async def register(
    user: UserCreate, 
    request: Request,
    db: Session = Depends(get_db)
):
    # 获取客户端IP地址
    client_ip = request.client.host
    
    # 清理用户输入，防止XSS
    username = UserValidator.sanitize_input(user.username)
    email = user.email.lower().strip()  # 邮箱转小写并去除首尾空格
    
    # 执行完整的安全校验
    validate_user_registration(
        username=username,
        email=email,
        password=user.password,
        ip_address=client_ip
    )
    
    # 检查用户是否已存在（邮箱）
    db_user = db.query(User).filter(User.email == email).first()
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="该邮箱已被注册"
        )
    
    # 检查用户名是否已存在
    db_user_by_name = db.query(User).filter(User.username == username).first()
    if db_user_by_name:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="该用户名已被使用"
        )
    
    # 记录注册信息（用于频率限制）
    record_registration(client_ip, email)
    
    # 创建新用户
    new_user = User(
        username=username,
        email=email,
        password=user.password
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.post("/login")
async def login(user: UserLogin, db: Session = Depends(get_db)):
    # 查找用户
    db_user = db.query(User).filter(User.email == user.email).first()
    if not db_user or not verify_password(user.password, db_user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="邮箱或密码错误",
            headers={"WWW-Authenticate": "Bearer"},
        )
    # 创建访问令牌
    access_token = create_access_token(data={"sub": db_user.email})
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/me", response_model=UserResponse)
async def get_current_user_info(current_user: User = Depends(get_current_user)):
    return current_user

@router.put("/me", response_model=UserResponse)
async def update_user_info(user_update: UserUpdate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    for field, value in user_update.model_dump(exclude_unset=True).items():
        setattr(current_user, field, value)
    db.commit()
    db.refresh(current_user)
    return current_user
