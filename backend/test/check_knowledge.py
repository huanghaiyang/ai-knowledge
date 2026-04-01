import os
import sys

# 添加 backend 目录到 Python 路径
backend_dir = os.path.join(os.path.dirname(__file__), "backend")
sys.path.append(backend_dir)

from app.utils.database import engine
from app.models.knowledge import KnowledgePoint
from sqlalchemy.orm import sessionmaker

# 会话工厂
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def check_knowledge_points():
    db = SessionLocal()
    try:
        # 查询知识点数据
        knowledge_points = db.query(KnowledgePoint).all()
        print(f"数据库中有 {len(knowledge_points)} 个知识点")
        
        # 打印前5个知识点
        print("前5个知识点:")
        for i, point in enumerate(knowledge_points[:5]):
            print(f"{i+1}. ID: {point.id}, 标题: {point.title}, 级别: {point.level}")
        
        # 搜索包含"机器学习"的知识点
        print("\n搜索包含'机器学习'的知识点:")
        ml_knowledge = db.query(KnowledgePoint).filter(
            KnowledgePoint.title.ilike("%机器学习%") | 
            KnowledgePoint.description.ilike("%机器学习%")
        ).all()
        for i, point in enumerate(ml_knowledge):
            print(f"{i+1}. ID: {point.id}, 标题: {point.title}, 描述: {point.description}")
            
        return len(knowledge_points)
    except Exception as e:
        print(f"查询数据库失败: {e}")
        return 0
    finally:
        db.close()

if __name__ == "__main__":
    check_knowledge_points()
