from passlib.context import CryptContext

# 密码加密上下文，使用内置的pbkdf2_sha256算法
pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")

def get_password_hash(password: str) -> str:
    # bcrypt限制密码长度为72字节，超过会被截断
    password = password[:72]
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)