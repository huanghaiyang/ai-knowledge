from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.utils.config import DB_USER, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME

# 明确使用pg8000驱动
DATABASE_URL = f"postgresql+pg8000://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# 创建数据库引擎，配置连接池
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    pool_size=20,  # 连接池大小
    max_overflow=40,  # 最大溢出连接数
    pool_timeout=60,  # 连接超时时间（秒）
    pool_recycle=1800,  # 连接回收时间（秒），避免连接过期
    echo=False  # 是否打印SQL语句
)

# 创建会话工厂
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 创建基类
Base = declarative_base()

# 依赖项，用于获取数据库会话
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        # 无论成功与否，都关闭会话
        db.close()
