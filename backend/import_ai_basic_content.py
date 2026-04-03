import os
import sys

# 添加当前目录到 Python 路径
sys.path.append(os.path.dirname(__file__))

from knowledge_content_manager import save_knowledge_content

def import_ai_basic_content():
    """从Markdown文件导入AI基础概念的教学内容"""
    # Markdown文件目录
    md_dir = os.path.join(os.path.dirname(__file__), 'content', 'markdown')
    
    # 知识点标题和对应的Markdown文件
    knowledge_files = {
        "人工智能定义与发展": "人工智能定义与发展.md",
        "机器学习基础": "机器学习基础.md",
        "深度学习基础": "深度学习基础.md",
        "自然语言处理": "自然语言处理.md",
        "计算机视觉": "计算机视觉.md",
        "人工智能伦理与安全": "人工智能伦理与安全.md"
    }
    
    # 导入每个知识点的内容
    for knowledge_title, md_file in knowledge_files.items():
        md_path = os.path.join(md_dir, md_file)
        if os.path.exists(md_path):
            print(f"导入知识点: {knowledge_title}")
            save_knowledge_content(knowledge_title, md_path)
        else:
            print(f"未找到Markdown文件: {md_path}")
    
    print("所有知识点的教学内容已导入")

if __name__ == "__main__":
    import_ai_basic_content()
