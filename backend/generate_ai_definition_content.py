import os
import sys

# 添加当前目录到 Python 路径
sys.path.append(os.path.dirname(__file__))

from sqlalchemy.orm import Session
from app.utils.database import engine, SessionLocal
from app.models.knowledge import KnowledgePoint
from app.models.content import KnowledgeContent

# 解析 Markdown 文件
def parse_markdown_content(markdown_file):
    """从 Markdown 文件中解析章节内容"""
    content_sections = []
    
    with open(markdown_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    current_section = None
    current_content = []
    
    for line in lines:
        line = line.strip()
        
        # 检查是否是一级或二级标题
        if line.startswith('# '):
            # 保存当前章节（如果存在）
            if current_section:
                content_sections.append({
                    "section_title": current_section,
                    "content": '\n'.join(current_content)
                })
            # 开始新章节
            current_section = line[2:].strip()
            current_content = []
        elif line.startswith('## '):
            # 保存当前章节（如果存在）
            if current_section:
                content_sections.append({
                    "section_title": current_section,
                    "content": '\n'.join(current_content)
                })
            # 开始新章节
            current_section = line[3:].strip()
            current_content = []
        else:
            # 添加内容到当前章节
            if current_section:
                current_content.append(line)
    
    # 保存最后一个章节
    if current_section:
        content_sections.append({
            "section_title": current_section,
            "content": '\n'.join(current_content)
        })
    
    return content_sections

# 为【人工智能定义】知识点生成详细的教学内容
def generate_ai_definition_content():
    # 创建数据库会话
    db = SessionLocal()
    
    try:
        # 查找【人工智能定义】知识点
        ai_definition_knowledge = db.query(KnowledgePoint).filter(
            KnowledgePoint.title == "人工智能定义"
        ).first()
        
        if not ai_definition_knowledge:
            print("未找到【人工智能的定义】知识点")
            return
        
        # 检查是否已经存在教学内容
        existing_content = db.query(KnowledgeContent).filter(
            KnowledgeContent.knowledge_id == ai_definition_knowledge.id
        ).count()
        
        if existing_content > 0:
            print("【人工智能的定义】知识点已经有教学内容，跳过创建")
            return
        
        # 从 Markdown 文件中读取教学内容
        markdown_file = os.path.join(os.path.dirname(__file__), 'ai_definition_content.md')
        content_sections = parse_markdown_content(markdown_file)
        
        # 插入教学内容
        for i, section in enumerate(content_sections):
            content = KnowledgeContent(
                knowledge_id=ai_definition_knowledge.id,
                section_title=section["section_title"],
                content=section["content"],
                order=i + 1
            )
            db.add(content)
        
        db.commit()
        print("【人工智能的定义】知识点的教学内容创建成功！")
    except Exception as e:
        print(f"创建教学内容失败: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    generate_ai_definition_content()
