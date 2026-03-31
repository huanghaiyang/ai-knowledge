import os
from sqlalchemy import create_engine, text
from app.utils.database import Base, engine
from app.models import user, knowledge, question, answer

# 创建所有表
Base.metadata.create_all(bind=engine)
print("数据库表创建成功！")

# 插入初始数据
from sqlalchemy.orm import Session
from app.models.knowledge import KnowledgePoint

# 连接数据库会话
db = Session(bind=engine)

# 检查是否已有数据
if db.query(KnowledgePoint).count() == 0:
    # 插入AI知识体系的一级知识点
    level1_knowledge = [
        {"title": "AI基础概念", "description": "人工智能的基本概念、发展历史和应用领域", "level": 1},
        {"title": "数学基础", "description": "线性代数、概率统计、微积分等AI所需的数学知识", "level": 1},
        {"title": "Python与数据处理", "description": "Python编程基础和数据处理库的使用", "level": 1},
        {"title": "机器学习算法", "description": "各种机器学习算法的原理和应用", "level": 1},
        {"title": "深度学习基础", "description": "深度学习的基本概念和神经网络基础", "level": 1},
        {"title": "大模型（LLM）原理与应用", "description": "大型语言模型的原理和应用", "level": 1},
        {"title": "计算机视觉CV", "description": "计算机视觉的基本概念和技术", "level": 1},
        {"title": "自然语言处理NLP", "description": "自然语言处理的基本概念和技术", "level": 1},
        {"title": "AI工具使用", "description": "TensorFlow、PyTorch等AI框架的使用", "level": 1},
        {"title": "AI行业与伦理", "description": "AI行业发展趋势和伦理问题", "level": 1}
    ]
    
    # 插入一级知识点
    level1_ids = []
    for item in level1_knowledge:
        knowledge_point = KnowledgePoint(**item)
        db.add(knowledge_point)
        db.commit()
        db.refresh(knowledge_point)
        level1_ids.append(knowledge_point.id)
    
    # 插入二级知识点
    level2_knowledge = [
        # AI基础概念
        {"title": "人工智能定义", "description": "人工智能的定义和内涵", "parent_id": level1_ids[0], "level": 2},
        {"title": "AI发展历史", "description": "人工智能的发展历程和重要里程碑", "parent_id": level1_ids[0], "level": 2},
        {"title": "AI应用领域", "description": "人工智能在各个领域的应用", "parent_id": level1_ids[0], "level": 2},
        
        # 数学基础
        {"title": "线性代数", "description": "向量、矩阵、线性变换等线性代数知识", "parent_id": level1_ids[1], "level": 2},
        {"title": "概率统计", "description": "概率、统计分布、假设检验等知识", "parent_id": level1_ids[1], "level": 2},
        {"title": "微积分", "description": "导数、积分、梯度等微积分知识", "parent_id": level1_ids[1], "level": 2},
        
        # Python与数据处理
        {"title": "Python基础", "description": "Python语法和编程基础", "parent_id": level1_ids[2], "level": 2},
        {"title": "NumPy", "description": "NumPy库的使用", "parent_id": level1_ids[2], "level": 2},
        {"title": "Pandas", "description": "Pandas库的使用", "parent_id": level1_ids[2], "level": 2},
        
        # 机器学习算法
        {"title": "监督学习", "description": "分类、回归等监督学习算法", "parent_id": level1_ids[3], "level": 2},
        {"title": "无监督学习", "description": "聚类、降维等无监督学习算法", "parent_id": level1_ids[3], "level": 2},
        {"title": "强化学习", "description": "强化学习算法和应用", "parent_id": level1_ids[3], "level": 2},
        
        # 深度学习基础
        {"title": "神经网络基础", "description": "神经网络的基本结构和原理", "parent_id": level1_ids[4], "level": 2},
        {"title": "激活函数", "description": "各种激活函数的特点和应用", "parent_id": level1_ids[4], "level": 2},
        {"title": "损失函数", "description": "各种损失函数的特点和应用", "parent_id": level1_ids[4], "level": 2},
        
        # 大模型（LLM）原理与应用
        {"title": "Transformer结构", "description": "Transformer模型的结构和原理", "parent_id": level1_ids[5], "level": 2},
        {"title": "预训练技术", "description": "预训练模型的技术和方法", "parent_id": level1_ids[5], "level": 2},
        {"title": "大模型应用", "description": "大模型在各个领域的应用", "parent_id": level1_ids[5], "level": 2},
        
        # 计算机视觉CV
        {"title": "图像处理", "description": "图像预处理和基本操作", "parent_id": level1_ids[6], "level": 2},
        {"title": "目标检测", "description": "目标检测算法和应用", "parent_id": level1_ids[6], "level": 2},
        {"title": "图像分类", "description": "图像分类算法和应用", "parent_id": level1_ids[6], "level": 2},
        
        # 自然语言处理NLP
        {"title": "文本预处理", "description": "文本的清洗和预处理", "parent_id": level1_ids[7], "level": 2},
        {"title": "词嵌入", "description": "词嵌入技术和应用", "parent_id": level1_ids[7], "level": 2},
        {"title": "文本分类", "description": "文本分类算法和应用", "parent_id": level1_ids[7], "level": 2},
        
        # AI工具使用
        {"title": "TensorFlow", "description": "TensorFlow框架的使用", "parent_id": level1_ids[8], "level": 2},
        {"title": "PyTorch", "description": "PyTorch框架的使用", "parent_id": level1_ids[8], "level": 2},
        {"title": "Scikit-learn", "description": "Scikit-learn库的使用", "parent_id": level1_ids[8], "level": 2},
        
        # AI行业与伦理
        {"title": "AI行业趋势", "description": "人工智能行业的发展趋势", "parent_id": level1_ids[9], "level": 2},
        {"title": "AI伦理问题", "description": "人工智能的伦理挑战和解决方案", "parent_id": level1_ids[9], "level": 2},
        {"title": "AI法律法规", "description": "与人工智能相关的法律法规", "parent_id": level1_ids[9], "level": 2}
    ]
    
    # 插入二级知识点
    for item in level2_knowledge:
        knowledge_point = KnowledgePoint(**item)
        db.add(knowledge_point)
    
    db.commit()
    print("初始数据插入成功！")
else:
    print("数据库已有数据，跳过初始数据插入。")

# 关闭数据库会话
db.close()
