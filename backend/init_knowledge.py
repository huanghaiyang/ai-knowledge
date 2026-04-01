import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.utils.database import engine, SessionLocal, Base
from app.models.knowledge import KnowledgePoint

# 学习模块分类
knowledge_categories = [
    {
        "title": "AI 基础概念",
        "description": "人工智能的基本概念、发展历史和应用领域",
        "level": 1
    },
    {
        "title": "数学基础",
        "description": "线性代数、概率统计、微积分等AI所需的数学知识",
        "level": 1,
        "children": [
            {
                "title": "线性代数",
                "description": "向量、矩阵、线性变换等基础概念",
                "level": 2
            },
            {
                "title": "概率统计",
                "description": "概率分布、统计推断、假设检验等",
                "level": 2
            },
            {
                "title": "微积分",
                "description": "导数、积分、优化等基础概念",
                "level": 2
            }
        ]
    },
    {
        "title": "Python 与数据处理",
        "description": "Python编程基础和数据处理工具",
        "level": 1
    },
    {
        "title": "机器学习算法",
        "description": "各类机器学习算法的原理和应用",
        "level": 1
    },
    {
        "title": "深度学习基础",
        "description": "神经网络基础、反向传播等",
        "level": 1
    },
    {
        "title": "大模型（LLM）原理与应用",
        "description": "大型语言模型的原理、训练和应用",
        "level": 1
    },
    {
        "title": "计算机视觉 CV",
        "description": "图像识别、目标检测等计算机视觉技术",
        "level": 1
    },
    {
        "title": "自然语言处理 NLP",
        "description": "文本处理、情感分析、机器翻译等NLP技术",
        "level": 1
    },
    {
        "title": "AI 工具使用",
        "description": "TensorFlow、PyTorch等AI框架的使用",
        "level": 1,
        "children": [
            {
                "title": "TensorFlow",
                "description": "Google开源的深度学习框架",
                "level": 2
            },
            {
                "title": "PyTorch",
                "description": "Facebook开源的深度学习框架",
                "level": 2
            }
        ]
    },
    {
        "title": "AI 行业与伦理",
        "description": "AI在各行业的应用和伦理问题",
        "level": 1
    }
]

def init_knowledge_points():
    """初始化知识模块分类"""
    # 创建数据库表
    Base.metadata.create_all(bind=engine)
    
    # 创建数据库会话
    db = SessionLocal()
    
    try:
        # 检查是否已经存在知识模块
        existing_count = db.query(KnowledgePoint).count()
        if existing_count > 0:
            print(f"知识模块已存在，共 {existing_count} 个，跳过初始化")
            return
        
        # 插入知识模块
        for category in knowledge_categories:
            # 创建一级分类
            parent = KnowledgePoint(
                title=category["title"],
                description=category["description"],
                level=category["level"]
            )
            db.add(parent)
            db.flush()  # 获取parent的id
            
            # 插入子分类
            if "children" in category:
                for child in category["children"]:
                    child_point = KnowledgePoint(
                        title=child["title"],
                        description=child["description"],
                        parent_id=parent.id,
                        level=child["level"]
                    )
                    db.add(child_point)
        
        # 提交事务
        db.commit()
        print("知识模块初始化完成")
        
    except Exception as e:
        print(f"初始化知识模块失败: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    init_knowledge_points()
