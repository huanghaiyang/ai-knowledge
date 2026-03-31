from sqlalchemy.orm import Session
from app.models.user import User
from app.models.answer import UserAnswer
from app.models.knowledge import KnowledgePoint
from collections import defaultdict

def generate_learning_report(user_id: int, db: Session) -> dict:
    """
    生成用户学习报告
    """
    # 获取用户信息
    user = db.query(User).filter(User.id == user_id).first()
    
    # 获取用户答题记录
    user_answers = db.query(UserAnswer).filter(UserAnswer.user_id == user_id).all()
    
    # 计算统计数据
    total_questions = len(user_answers)
    correct_questions = sum(1 for ua in user_answers if ua.is_correct)
    accuracy = correct_questions / total_questions if total_questions > 0 else 0
    
    # 按知识点统计
    knowledge_stats = defaultdict(lambda: {"total": 0, "correct": 0})
    for ua in user_answers:
        question = ua.question
        if question and question.knowledge:
            knowledge_id = question.knowledge.id
            knowledge_stats[knowledge_id]["total"] += 1
            if ua.is_correct:
                knowledge_stats[knowledge_id]["correct"] += 1
    
    # 计算各知识点掌握度
    knowledge_mastery = {}
    for knowledge_id, stats in knowledge_stats.items():
        knowledge = db.query(KnowledgePoint).filter(KnowledgePoint.id == knowledge_id).first()
        if knowledge:
            mastery = stats["correct"] / stats["total"] if stats["total"] > 0 else 0
            knowledge_mastery[knowledge.title] = mastery
    
    # 生成报告
    report = {
        "user_id": user_id,
        "username": user.username,
        "total_questions": total_questions,
        "correct_questions": correct_questions,
        "accuracy": accuracy,
        "learning_hours": user.learning_hours,
        "knowledge_mastery": knowledge_mastery,
        "recommended_learning": generate_recommendations(knowledge_mastery)
    }
    
    return report

def generate_weak_points(user_id: int, db: Session) -> list:
    """
    生成用户薄弱知识点
    """
    # 获取用户答题记录
    user_answers = db.query(UserAnswer).filter(UserAnswer.user_id == user_id).all()
    
    # 按知识点统计错误率
    knowledge_errors = defaultdict(lambda: {"total": 0, "incorrect": 0})
    for ua in user_answers:
        question = ua.question
        if question and question.knowledge:
            knowledge_id = question.knowledge.id
            knowledge_errors[knowledge_id]["total"] += 1
            if not ua.is_correct:
                knowledge_errors[knowledge_id]["incorrect"] += 1
    
    # 计算各知识点错误率
    weak_points = []
    for knowledge_id, stats in knowledge_errors.items():
        knowledge = db.query(KnowledgePoint).filter(KnowledgePoint.id == knowledge_id).first()
        if knowledge:
            error_rate = stats["incorrect"] / stats["total"] if stats["total"] > 0 else 0
            if error_rate > 0.5:  # 错误率超过50%的视为薄弱知识点
                weak_points.append({
                    "knowledge_id": knowledge_id,
                    "knowledge_title": knowledge.title,
                    "error_rate": error_rate,
                    "total_questions": stats["total"],
                    "incorrect_questions": stats["incorrect"]
                })
    
    # 按错误率排序
    weak_points.sort(key=lambda x: x["error_rate"], reverse=True)
    
    return weak_points

def generate_recommendations(knowledge_mastery: dict) -> list:
    """
    根据知识点掌握度生成学习推荐
    """
    recommendations = []
    
    # 按掌握度排序，找出掌握度低的知识点
    sorted_knowledge = sorted(knowledge_mastery.items(), key=lambda x: x[1])
    
    # 推荐掌握度最低的3个知识点
    for knowledge_title, mastery in sorted_knowledge[:3]:
        recommendations.append({
            "knowledge_title": knowledge_title,
            "mastery": mastery,
            "recommendation": f"建议加强{knowledge_title}的学习"
        })
    
    return recommendations
