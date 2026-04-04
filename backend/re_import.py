#!/usr/bin/env python3
"""重新导入所有知识点内容"""

import os
import sys

# 添加当前目录到 Python 路径
sys.path.append(os.path.dirname(__file__))

from import_ai_basic_content import import_ai_basic_content
from import_level3_content import import_level3_content
from sqlalchemy.orm import Session
from app.utils.database import engine
from app.models.content import KnowledgeContent

def clear_knowledge_content():
    """清理知识点内容表"""
    print("\n清理知识点内容表...")
    try:
        db = Session(bind=engine)
        # 删除所有知识点内容记录
        deleted_count = db.query(KnowledgeContent).delete()
        db.commit()
        print(f"成功清理 {deleted_count} 条知识点内容记录")
        return True
    except Exception as e:
        print(f"清理知识点内容表时发生错误: {e}")
        return False

def re_import_all_content():
    """重新导入所有知识点内容"""
    print("=" * 60)
    print("开始重新导入所有知识点内容")
    print("=" * 60)
    
    try:
        # 清理知识点内容表
        if not clear_knowledge_content():
            print("清理知识点内容表失败，导入过程中止")
            return False
        
        # 导入二级知识点
        print("\n1. 导入二级知识点...")
        import_ai_basic_content()
        
        # 导入三级知识点
        print("\n2. 导入三级知识点...")
        import_level3_content()
        
        print("\n" + "=" * 60)
        print("所有知识点内容导入完成！")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n导入过程中发生错误: {e}")
        print("请检查错误信息并修复后重试")
        print("=" * 60)
        return False
    
    return True

if __name__ == "__main__":
    re_import_all_content()
