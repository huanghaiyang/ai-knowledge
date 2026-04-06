import os
from sqlalchemy import create_engine, text
from app.utils.database import Base, engine
from app.models import user, knowledge, question, answer
from app.models.content import KnowledgeContent
from app.models.highlight import KnowledgeHighlight

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
        {"title": "AI基础概念", "description": "人工智能的基本概念、发展历史和应用领域", "level": 1, "order": 1},
        {"title": "数学基础", "description": "线性代数、概率统计、微积分等AI所需的数学知识", "level": 1, "order": 2},
        {"title": "Python与数据处理", "description": "Python编程基础和数据处理库的使用", "level": 1, "order": 3},
        {"title": "机器学习算法", "description": "各种机器学习算法的原理和应用", "level": 1, "order": 4},
        {"title": "深度学习基础", "description": "深度学习的基本概念和神经网络基础", "level": 1, "order": 5},
        {"title": "大模型（LLM）原理与应用", "description": "大型语言模型的原理和应用", "level": 1, "order": 6},
        {"title": "计算机视觉CV", "description": "计算机视觉的基本概念和技术", "level": 1, "order": 7},
        {"title": "自然语言处理NLP", "description": "自然语言处理的基本概念和技术", "level": 1, "order": 8},
        {"title": "AI工具使用", "description": "TensorFlow、PyTorch等AI框架的使用", "level": 1, "order": 9},
        {"title": "AI行业与伦理", "description": "AI行业发展趋势和伦理问题", "level": 1, "order": 10}
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
        {"title": "人工智能定义与发展", "description": "人工智能的定义、发展历程和主要里程碑", "parent_id": level1_ids[0], "level": 2, "order": 1},
        {"title": "机器学习基础", "description": "机器学习的基本概念、算法和应用", "parent_id": level1_ids[0], "level": 2, "order": 2},
        {"title": "深度学习基础", "description": "深度学习的基本概念、网络结构和应用", "parent_id": level1_ids[0], "level": 2, "order": 3},
        {"title": "自然语言处理", "description": "自然语言处理的基本概念、技术和应用", "parent_id": level1_ids[0], "level": 2, "order": 4},
        {"title": "计算机视觉", "description": "计算机视觉的基本概念、技术和应用", "parent_id": level1_ids[0], "level": 2, "order": 5},
        {"title": "人工智能伦理与安全", "description": "人工智能的伦理问题、安全挑战和监管政策", "parent_id": level1_ids[0], "level": 2, "order": 6},
        
        # 数学基础
        {"title": "线性代数", "description": "向量、矩阵、线性变换等线性代数知识", "parent_id": level1_ids[1], "level": 2, "order": 7},
        {"title": "概率统计", "description": "概率、统计分布、假设检验等知识", "parent_id": level1_ids[1], "level": 2, "order": 8},
        {"title": "微积分", "description": "导数、积分、梯度等微积分知识", "parent_id": level1_ids[1], "level": 2, "order": 9},
        
        # Python与数据处理
        {"title": "Python基础", "description": "Python语法和编程基础", "parent_id": level1_ids[2], "level": 2, "order": 10},
        {"title": "NumPy", "description": "NumPy库的使用", "parent_id": level1_ids[2], "level": 2, "order": 11},
        {"title": "Pandas", "description": "Pandas库的使用", "parent_id": level1_ids[2], "level": 2, "order": 12},
        
        # 机器学习算法
        {"title": "监督学习", "description": "分类、回归等监督学习算法", "parent_id": level1_ids[3], "level": 2, "order": 13},
        {"title": "无监督学习", "description": "聚类、降维等无监督学习算法", "parent_id": level1_ids[3], "level": 2, "order": 14},
        {"title": "强化学习", "description": "强化学习算法和应用", "parent_id": level1_ids[3], "level": 2, "order": 15},
        
        # 深度学习基础
        {"title": "神经网络基础", "description": "神经网络的基本结构和原理", "parent_id": level1_ids[4], "level": 2, "order": 16},
        {"title": "激活函数", "description": "各种激活函数的特点和应用", "parent_id": level1_ids[4], "level": 2, "order": 17},
        {"title": "损失函数", "description": "各种损失函数的特点和应用", "parent_id": level1_ids[4], "level": 2, "order": 18},
        
        # 大模型（LLM）原理与应用
        {"title": "Transformer结构", "description": "Transformer模型的结构和原理", "parent_id": level1_ids[5], "level": 2, "order": 19},
        {"title": "预训练技术", "description": "预训练模型的技术和方法", "parent_id": level1_ids[5], "level": 2, "order": 20},
        {"title": "大模型应用", "description": "大模型在各个领域的应用", "parent_id": level1_ids[5], "level": 2, "order": 21},
        
        # 计算机视觉CV
        {"title": "图像处理", "description": "图像预处理和基本操作", "parent_id": level1_ids[6], "level": 2, "order": 22},
        {"title": "目标检测", "description": "目标检测算法和应用", "parent_id": level1_ids[6], "level": 2, "order": 23},
        {"title": "图像分类", "description": "图像分类算法和应用", "parent_id": level1_ids[6], "level": 2, "order": 24},
        
        # 自然语言处理NLP
        {"title": "文本预处理", "description": "文本的清洗和预处理", "parent_id": level1_ids[7], "level": 2, "order": 25},
        {"title": "词嵌入", "description": "词嵌入技术和应用", "parent_id": level1_ids[7], "level": 2, "order": 26},
        {"title": "文本分类", "description": "文本分类算法和应用", "parent_id": level1_ids[7], "level": 2, "order": 27},
        
        # AI工具使用
        {"title": "TensorFlow", "description": "TensorFlow框架的使用", "parent_id": level1_ids[8], "level": 2, "order": 28},
        {"title": "PyTorch", "description": "PyTorch框架的使用", "parent_id": level1_ids[8], "level": 2, "order": 29},
        {"title": "Scikit-learn", "description": "Scikit-learn库的使用", "parent_id": level1_ids[8], "level": 2, "order": 30},
        
        # AI行业与伦理
        {"title": "AI行业趋势", "description": "人工智能行业的发展趋势", "parent_id": level1_ids[9], "level": 2, "order": 31},
        {"title": "AI伦理问题", "description": "人工智能的伦理挑战和解决方案", "parent_id": level1_ids[9], "level": 2, "order": 32},
        {"title": "AI法律法规", "description": "与人工智能相关的法律法规", "parent_id": level1_ids[9], "level": 2, "order": 33}
    ]
    
    # 插入二级知识点
    level2_ids = {}
    for item in level2_knowledge:
        knowledge_point = KnowledgePoint(**item)
        db.add(knowledge_point)
        db.flush()  # 获取id但不提交事务
        level2_ids[item["title"]] = knowledge_point.id
    
    # 为AI基础概念模块生成详细的三级知识点
    level3_knowledge = [
        # 人工智能定义与发展
        {"title": "人工智能的定义", "description": "人工智能是指计算机系统执行通常需要人类智能的任务的能力，包括学习、推理、问题解决、感知和语言理解等。", "parent_id": level2_ids["人工智能定义与发展"], "level": 3, "order": 1},
        {"title": "人工智能的发展历程", "description": "从图灵测试到深度学习，人工智能的发展经历了多个阶段，包括早期的符号主义、连接主义、专家系统，以及近年来的深度学习革命。", "parent_id": level2_ids["人工智能定义与发展"], "level": 3, "order": 2},
        {"title": "人工智能的主要分支", "description": "人工智能包括机器学习、深度学习、自然语言处理、计算机视觉、机器人学等多个分支领域。", "parent_id": level2_ids["人工智能定义与发展"], "level": 3, "order": 3},
        {"title": "人工智能的应用领域", "description": "人工智能已经广泛应用于医疗、金融、教育、交通、制造业等多个领域，正在改变人们的生活和工作方式。", "parent_id": level2_ids["人工智能定义与发展"], "level": 3, "order": 4},
        
        # 机器学习基础
        {"title": "机器学习的定义", "description": "机器学习是人工智能的一个分支，通过算法使计算机从数据中学习，而不是通过明确编程。", "parent_id": level2_ids["机器学习基础"], "level": 3, "order": 5},
        {"title": "机器学习的类型", "description": "机器学习包括监督学习、无监督学习、半监督学习和强化学习等多种类型。", "parent_id": level2_ids["机器学习基础"], "level": 3, "order": 6},
        {"title": "机器学习的基本流程", "description": "机器学习的基本流程包括数据收集、数据预处理、特征工程、模型训练、模型评估和模型部署等步骤。", "parent_id": level2_ids["机器学习基础"], "level": 3, "order": 7},
        {"title": "机器学习的常见算法", "description": "常见的机器学习算法包括线性回归、逻辑回归、决策树、随机森林、支持向量机、K近邻等。", "parent_id": level2_ids["机器学习基础"], "level": 3, "order": 8},
        
        # 深度学习基础
        {"title": "深度学习的定义", "description": "深度学习是机器学习的一个分支，使用多层神经网络来模拟人脑的学习过程，能够自动提取数据中的特征。", "parent_id": level2_ids["深度学习基础"], "level": 3, "order": 9},
        {"title": "神经网络的基本结构", "description": "神经网络由输入层、隐藏层和输出层组成，每层包含多个神经元，神经元之间通过权重连接。", "parent_id": level2_ids["深度学习基础"], "level": 3, "order": 10},
        {"title": "深度学习的常见模型", "description": "常见的深度学习模型包括卷积神经网络(CNN)、循环神经网络(RNN)、长短期记忆网络(LSTM)、Transformer等。", "parent_id": level2_ids["深度学习基础"], "level": 3, "order": 11},
        {"title": "深度学习的训练方法", "description": "深度学习的训练方法包括反向传播算法、梯度下降优化器、正则化技术等。", "parent_id": level2_ids["深度学习基础"], "level": 3, "order": 12},
        
        # 自然语言处理
        {"title": "自然语言处理的定义", "description": "自然语言处理是人工智能的一个分支，研究如何使计算机理解、处理和生成人类语言。", "parent_id": level2_ids["自然语言处理"], "level": 3, "order": 13},
        {"title": "自然语言处理的主要任务", "description": "自然语言处理的主要任务包括分词、词性标注、命名实体识别、情感分析、机器翻译、问答系统等。", "parent_id": level2_ids["自然语言处理"], "level": 3, "order": 14},
        {"title": "自然语言处理的技术方法", "description": "自然语言处理的技术方法包括规则-based方法、统计方法和深度学习方法。", "parent_id": level2_ids["自然语言处理"], "level": 3, "order": 15},
        {"title": "自然语言处理的应用", "description": "自然语言处理的应用包括智能客服、机器翻译、文本摘要、情感分析、聊天机器人等。", "parent_id": level2_ids["自然语言处理"], "level": 3, "order": 16},
        
        # 计算机视觉
        {"title": "计算机视觉的定义", "description": "计算机视觉是人工智能的一个分支，研究如何使计算机从图像或视频中提取信息和理解内容。", "parent_id": level2_ids["计算机视觉"], "level": 3, "order": 17},
        {"title": "计算机视觉的主要任务", "description": "计算机视觉的主要任务包括图像分类、目标检测、语义分割、目标跟踪、图像生成等。", "parent_id": level2_ids["计算机视觉"], "level": 3, "order": 18},
        {"title": "计算机视觉的技术方法", "description": "计算机视觉的技术方法包括传统的图像处理方法和基于深度学习的方法，如卷积神经网络。", "parent_id": level2_ids["计算机视觉"], "level": 3, "order": 19},
        {"title": "计算机视觉的应用", "description": "计算机视觉的应用包括人脸识别、物体识别、自动驾驶、医学影像分析、安防监控等。", "parent_id": level2_ids["计算机视觉"], "level": 3, "order": 20},
        
        # 人工智能伦理与安全
        {"title": "人工智能的伦理问题", "description": "人工智能的伦理问题包括隐私保护、算法偏见、就业影响、人机关系等。", "parent_id": level2_ids["人工智能伦理与安全"], "level": 3, "order": 21},
        {"title": "人工智能的安全挑战", "description": "人工智能的安全挑战包括对抗性攻击、模型中毒、数据泄露、AI系统的可解释性等。", "parent_id": level2_ids["人工智能伦理与安全"], "level": 3, "order": 22},
        {"title": "人工智能的监管政策", "description": "各国正在制定人工智能的监管政策，以确保AI的安全、公平和负责任的使用。", "parent_id": level2_ids["人工智能伦理与安全"], "level": 3, "order": 23},
        {"title": "人工智能的未来发展", "description": "人工智能的未来发展趋势包括通用人工智能(AGI)、人机协作、量子计算与AI的结合等。", "parent_id": level2_ids["人工智能伦理与安全"], "level": 3, "order": 24}
    ]
    
    # 插入三级知识点
    for item in level3_knowledge:
        knowledge_point = KnowledgePoint(**item)
        db.add(knowledge_point)
    
    db.commit()
    print("初始数据插入成功！")
else:
    print("数据库已有数据，跳过初始数据插入。")

# 关闭数据库会话
db.close()
