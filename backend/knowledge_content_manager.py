import os
import sys

# 添加当前目录到 Python 路径
sys.path.append(os.path.dirname(__file__))

from sqlalchemy.orm import Session
from app.utils.database import SessionLocal
from app.models.knowledge import KnowledgePoint
from app.models.content import KnowledgeContent

def parse_markdown_content(markdown_file):
    """从 Markdown 文件中解析章节内容"""
    content_sections = []
    
    with open(markdown_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    current_section = None
    current_content = []
    in_code_block = False  # 标记是否在代码块中
    
    for line in lines:
        stripped_line = line.strip()
        
        # 检查代码块的开始和结束
        if stripped_line.startswith('```'):
            in_code_block = not in_code_block
            current_content.append(line.rstrip())
            continue
        
        # 如果在代码块中，直接添加内容，不解析标题
        if in_code_block:
            current_content.append(line.rstrip())
            continue
        
        # 检查是否是一级或二级标题（不在代码块中）
        if stripped_line.startswith('# '):
            # 保存当前章节（如果存在）
            if current_section:
                content_sections.append({
                    "section_title": current_section,
                    "content": '\n'.join(current_content)
                })
            # 开始新章节
            current_section = stripped_line[2:].strip()
            current_content = []
        elif stripped_line.startswith('## '):
            # 保存当前章节（如果存在）
            if current_section:
                content_sections.append({
                    "section_title": current_section,
                    "content": '\n'.join(current_content)
                })
            # 开始新章节
            current_section = stripped_line[3:].strip()
            current_content = []
        else:
            # 添加内容到当前章节
            if current_section:
                current_content.append(line.rstrip())
    
    # 保存最后一个章节
    if current_section:
        content_sections.append({
            "section_title": current_section,
            "content": '\n'.join(current_content)
        })
    
    return content_sections

def save_knowledge_content(knowledge_title, markdown_file, parent_title=None):
    """保存知识点的教学内容到数据库"""
    db = SessionLocal()
    
    try:
        # 查找知识点
        knowledge_point = db.query(KnowledgePoint).filter(
            KnowledgePoint.title == knowledge_title
        ).first()
        
        if not knowledge_point:
            print(f"未找到【{knowledge_title}】知识点")
            return False
        
        # 检查是否已经存在教学内容
        existing_content = db.query(KnowledgeContent).filter(
            KnowledgeContent.knowledge_id == knowledge_point.id
        ).count()
        
        if existing_content > 0:
            print(f"【{knowledge_title}】知识点已经有教学内容，跳过创建")
            return True
        
        # 从 Markdown 文件中读取教学内容
        content_sections = parse_markdown_content(markdown_file)
        
        # 插入教学内容
        for i, section in enumerate(content_sections):
            content = KnowledgeContent(
                knowledge_id=knowledge_point.id,
                section_title=section["section_title"],
                content=section["content"],
                order=i + 1
            )
            db.add(content)
        
        db.commit()
        print(f"【{knowledge_title}】知识点的教学内容创建成功，共 {len(content_sections)} 个章节")
        return True
        
    except Exception as e:
        print(f"创建教学内容失败: {e}")
        db.rollback()
        return False
    finally:
        db.close()

def create_knowledge_point(title, description, parent_title=None, level=2):
    """创建知识点"""
    db = SessionLocal()
    
    try:
        # 查找父知识点
        parent_id = None
        if parent_title:
            parent = db.query(KnowledgePoint).filter(
                KnowledgePoint.title == parent_title
            ).first()
            if parent:
                parent_id = parent.id
        
        # 创建知识点
        knowledge_point = KnowledgePoint(
            title=title,
            description=description,
            parent_id=parent_id,
            level=level
        )
        db.add(knowledge_point)
        db.commit()
        db.refresh(knowledge_point)
        print(f"创建【{title}】知识点成功，ID: {knowledge_point.id}")
        return knowledge_point
        
    except Exception as e:
        print(f"创建知识点失败: {e}")
        db.rollback()
        return None
    finally:
        db.close()
