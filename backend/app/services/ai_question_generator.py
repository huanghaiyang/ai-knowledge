import openai
import os
import json
from dotenv import load_dotenv
from app.models.knowledge import KnowledgePoint
from sqlalchemy.orm import Session

load_dotenv()

# 配置OpenAI API
openai.api_key = os.getenv("OPENAI_API_KEY", "your-api-key")

def generate_ai_question(knowledge_id: int, difficulty: str, question_type: str) -> dict:
    """
    使用AI生成题目
    """
    # 这里简化处理，实际应用中应该从数据库获取知识点详情
    knowledge_title = "AI基础概念"  # 示例，实际应根据knowledge_id查询
    
    # 根据题目类型和难度生成不同的提示
    prompts = {
        "single_choice": f"生成一个关于{knowledge_title}的单选题，难度{difficulty}，包含4个选项，其中只有一个正确答案。",
        "multiple_choice": f"生成一个关于{knowledge_title}的多选题，难度{difficulty}，包含4个选项，其中有多个正确答案。",
        "true_false": f"生成一个关于{knowledge_title}的判断题，难度{difficulty}，判断对错。",
        "fill_blank": f"生成一个关于{knowledge_title}的填空题，难度{difficulty}，需要填写一个术语或公式。",
        "short_answer": f"生成一个关于{knowledge_title}的简答题，难度{difficulty}，需要简要回答问题。",
        "code": f"生成一个关于{knowledge_title}的代码题，难度{difficulty}，需要补全或编写简单代码。"
    }
    
    prompt = prompts.get(question_type, prompts["single_choice"])
    
    # 调用OpenAI API生成题目
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "你是一个AI教育专家，擅长生成高质量的AI知识题目。"},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7,
    )
    
    # 解析生成的题目
    # 注意：这里简化处理，实际应用中需要更复杂的解析逻辑
    question_content = response.choices[0].message.content
    
    # 构造返回数据
    question_data = {
        "knowledge_id": knowledge_id,
        "question_type": question_type,
        "difficulty": difficulty,
        "content": question_content,
        "options": json.dumps(["选项A", "选项B", "选项C", "选项D"]),  # 示例
        "correct_answer": "选项A",  # 示例
        "explanation": "这是题目的解析。"  # 示例
    }
    
    return question_data
