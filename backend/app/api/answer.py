from flask import request, jsonify, g
from sqlalchemy.orm import Session
from app.models.answer import Answer, UserAnswer
from app.utils.database import get_db
from app.utils.security import login_required, get_current_user
from app.services.ai_grader import grade_answer

async def submit_answer(data: dict, current_user_id: int, db: Session):
    # 检查题目是否存在
    question_id = data.get('question_id')
    user_answer = data.get('user_answer')
    question = db.query(Answer.question).filter(Answer.question_id == question_id).first()
    if not question:
        return jsonify({"detail": "题目不存在"}), 404
    
    # 自动批改
    is_correct, score, feedback = grade_answer(question_id, user_answer)
    
    # 保存用户答案
    new_user_answer = UserAnswer(
        user_id=current_user_id,
        question_id=question_id,
        user_answer=user_answer,
        is_correct=is_correct,
        score=score,
        feedback=feedback
    )
    db.add(new_user_answer)
    db.commit()
    db.refresh(new_user_answer)
    
    return jsonify({
        "id": new_user_answer.id,
        "user_id": new_user_answer.user_id,
        "question_id": new_user_answer.question_id,
        "user_answer": new_user_answer.user_answer,
        "is_correct": new_user_answer.is_correct,
        "score": new_user_answer.score,
        "feedback": new_user_answer.feedback,
        "created_at": new_user_answer.created_at
    })

async def get_user_answers(current_user_id: int, db: Session):
    user_answers = db.query(UserAnswer).filter(UserAnswer.user_id == current_user_id).all()
    return jsonify([
        {
            "id": ua.id,
            "user_id": ua.user_id,
            "question_id": ua.question_id,
            "user_answer": ua.user_answer,
            "is_correct": ua.is_correct,
            "score": ua.score,
            "feedback": ua.feedback,
            "created_at": ua.created_at
        } for ua in user_answers
    ])

async def get_incorrect_answers(current_user_id: int, db: Session):
    incorrect_answers = db.query(UserAnswer).filter(
        UserAnswer.user_id == current_user_id,
        UserAnswer.is_correct == False
    ).all()
    return jsonify([
        {
            "id": ua.id,
            "user_id": ua.user_id,
            "question_id": ua.question_id,
            "user_answer": ua.user_answer,
            "is_correct": ua.is_correct,
            "score": ua.score,
            "feedback": ua.feedback,
            "created_at": ua.created_at
        } for ua in incorrect_answers
    ])

def register_routes(app):
    @app.route('/api/answer/user-answer', methods=['POST'])
    @login_required
    async def flask_submit_answer():
        data = request.get_json()
        if not hasattr(g, 'db'):
            g.db = next(get_db())
        db = g.db
        try:
            return await submit_answer(data, g.current_user.id, db)
        finally:
            if hasattr(g, 'db'):
                g.db.close()
                delattr(g, 'db')
    
    @app.route('/api/answer/user-answers', methods=['GET'])
    @login_required
    async def flask_get_user_answers():
        if not hasattr(g, 'db'):
            g.db = next(get_db())
        db = g.db
        try:
            return await get_user_answers(g.current_user.id, db)
        finally:
            if hasattr(g, 'db'):
                g.db.close()
                delattr(g, 'db')
    
    @app.route('/api/answer/user-answers/incorrect', methods=['GET'])
    @login_required
    async def flask_get_incorrect_answers():
        if not hasattr(g, 'db'):
            g.db = next(get_db())
        db = g.db
        try:
            return await get_incorrect_answers(g.current_user.id, db)
        finally:
            if hasattr(g, 'db'):
                g.db.close()
                delattr(g, 'db')
