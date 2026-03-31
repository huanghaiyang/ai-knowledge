import openai
import os
from dotenv import load_dotenv
from app.models.question import Question
from sqlalchemy.orm import Session

load_dotenv()

# 配置OpenAI API
openai.api_key = os.getenv("OPENAI_API_KEY", "your-api-key")

def grade_answer(question_id: int, user_answer: str) -> tuple[bool, float, str]:
    """
    自动批改用户答案
    返回：(是否正确, 分数, 反馈)
    """
    # 这里简化处理，实际应用中应该从数据库获取题目详情
    # 示例题目信息
    question_type = "single_choice"  # 示例，实际应根据question_id查询
    correct_answer = "选项A"  # 示例，实际应根据question_id查询
    
    # 根据题目类型进行不同的批改逻辑
    if question_type in ["single_choice", "multiple_choice", "true_false"]:
        # 客观题批改
        is_correct = user_answer == correct_answer
        score = 1.0 if is_correct else 0.0
        feedback = "回答正确！" if is_correct else f"回答错误，正确答案是：{correct_answer}"
    else:
        # 主观题（简答题、代码题）使用AI批改
        prompt = f"请批改以下关于AI知识的回答。\n题目：[题目内容]\n正确答案：{correct_answer}\n用户回答：{user_answer}\n请判断是否正确，并给出分数（0-1）和详细反馈。"
        
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "你是一个AI教育专家，擅长批改AI知识题目。"},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
        )
        
        # 解析AI批改结果
        # 注意：这里简化处理，实际应用中需要更复杂的解析逻辑
        feedback = response.choices[0].message.content
        is_correct = "正确" in feedback
        score = 0.8 if is_correct else 0.4
    
    return is_correct, score, feedback
