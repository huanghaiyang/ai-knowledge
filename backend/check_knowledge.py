import os
import sys

# 添加当前目录到 Python 路径
sys.path.append(os.path.dirname(__file__))

from sqlalchemy.orm import Session
from app.utils.database import engine, SessionLocal
from app.models.knowledge import KnowledgePoint

# 检查数据库中的知识点结构
def check_knowledge_structure():
    # 创建数据库会话
    db = SessionLocal()
    
    try:
        # 获取所有知识点
        knowledge_points = db.query(KnowledgePoint).all()
        
        print("数据库中的知识点结构：")
        print("=" * 80)
        
        # 按层级打印知识点
        level1_points = [p for p in knowledge_points if p.level == 1]
        for level1 in level1_points:
            print(f"一级知识点: {level1.title} (id: {level1.id})")
            
            level2_points = [p for p in knowledge_points if p.parent_id == level1.id]
            for level2 in level2_points:
                print(f"  二级知识点: {level2.title} (id: {level2.id})")
                
                level3_points = [p for p in knowledge_points if p.parent_id == level2.id]
                for level3 in level3_points:
                    print(f"    三级知识点: {level3.title} (id: {level3.id})")
        
        print("=" * 80)
    except Exception as e:
        print(f"检查知识点结构失败: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    check_knowledge_structure()
