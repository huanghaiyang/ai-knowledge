import os
import sys
from dotenv import load_dotenv
from sqlalchemy import inspect

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.utils.database import engine, Base, SessionLocal
from app.models.user import User

# 加载环境变量
load_dotenv()

print("Testing database connection...")

# 测试数据库连接
try:
    # 测试连接
    with engine.connect() as connection:
        print("✅ Database connection successful!")
    
    # 检查users表是否存在
    inspector = inspect(engine)
    if inspector.has_table("users"):
        print("✅ Users table exists!")
    else:
        print("❌ Users table does not exist!")
        # 尝试创建表
        print("Creating tables...")
        Base.metadata.create_all(bind=engine)
        print("✅ Tables created successfully!")
    
    # 测试会话
    db = SessionLocal()
    try:
        # 尝试查询用户
        users = db.query(User).all()
        print(f"✅ User query successful, found {len(users)} users")
    finally:
        db.close()
        
except Exception as e:
    print(f"❌ Database connection failed: {e}")