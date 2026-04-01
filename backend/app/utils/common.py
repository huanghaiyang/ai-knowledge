from passlib.context import CryptContext

# 密码加密上下文，使用更安全的argon2算法
pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

def get_password_hash(password: str) -> str:
    # argon2限制密码长度为4096字节，超过会被截断
    password = password[:4096]
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)