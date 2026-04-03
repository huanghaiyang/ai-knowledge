from flask import request, jsonify
from sqlalchemy.orm import Session
from app.models.question import Question
from app.utils.database import get_db
from app.utils.security import get_current_user
from app.utils.validators import QuestionValidator, UserValidator
from app.services.ai_question_generator import generate_ai_question

async def get_questions(knowledge_id: int, difficulty: str, db: Session):
    query = db.query(Question)
    if knowledge_id:
        query = query.filter(Question.knowledge_id == knowledge_id)
    if difficulty:
        query = query.filter(Question.difficulty == difficulty)
    questions = query.all()
    return jsonify([
        {
            "id": q.id,
            "content": q.content,
            "options": q.options,
            "correct_answer": q.correct_answer,
            "knowledge_id": q.knowledge_id,
            "difficulty": q.difficulty,
            "question_type": q.question_type
        } for q in questions
    ])

async def get_question(question_id: int, db: Session):
    question = db.query(Question).filter(Question.id == question_id).first()
    if not question:
        return jsonify({"detail": "题目不存在"}), 404
    return jsonify({
        "id": question.id,
        "content": question.content,
        "options": question.options,
        "correct_answer": question.correct_answer,
        "knowledge_id": question.knowledge_id,
        "difficulty": question.difficulty,
        "question_type": question.question_type
    })

async def generate_question(knowledge_id: int, difficulty: str, question_type: str, db: Session):
    # 使用AI生成题目
    question_data = generate_ai_question(knowledge_id, difficulty, question_type)
    new_question = Question(**question_data)
    db.add(new_question)
    db.commit()
    db.refresh(new_question)
    return jsonify({
        "id": new_question.id,
        "content": new_question.content,
        "options": new_question.options,
        "correct_answer": new_question.correct_answer,
        "knowledge_id": new_question.knowledge_id,
        "difficulty": new_question.difficulty,
        "question_type": new_question.question_type
    })

async def create_question(data: dict, db: Session):
    # 清理和验证输入
    content = UserValidator.sanitize_input(data.get('content', ''))
    options = UserValidator.sanitize_input(data.get('options', ''))
    correct_answer = UserValidator.sanitize_input(data.get('correct_answer', ''))
    knowledge_id = data.get('knowledge_id')
    difficulty = data.get('difficulty')
    question_type = data.get('question_type')
    
    # 验证题目内容
    is_valid, message = QuestionValidator.validate_content(content)
    if not is_valid:
        return jsonify({"detail": message}), 400
    
    # 验证题目选项
    is_valid, message = QuestionValidator.validate_options(options)
    if not is_valid:
        return jsonify({"detail": message}), 400
    
    # 验证正确答案
    is_valid, message = QuestionValidator.validate_answer(correct_answer)
    if not is_valid:
        return jsonify({"detail": message}), 400
    
    # 验证题目类型
    is_valid, message = QuestionValidator.validate_question_type(question_type)
    if not is_valid:
        return jsonify({"detail": message}), 400
    
    # 验证难度级别
    is_valid, message = QuestionValidator.validate_difficulty(difficulty)
    if not is_valid:
        return jsonify({"detail": message}), 400
    
    new_question = Question(
        content=content,
        options=options,
        correct_answer=correct_answer,
        knowledge_id=knowledge_id,
        difficulty=difficulty,
        question_type=question_type
    )
    db.add(new_question)
    db.commit()
    db.refresh(new_question)
    return jsonify({
        "id": new_question.id,
        "content": new_question.content,
        "options": new_question.options,
        "correct_answer": new_question.correct_answer,
        "knowledge_id": new_question.knowledge_id,
        "difficulty": new_question.difficulty,
        "question_type": new_question.question_type
    })

async def update_question(question_id: int, data: dict, db: Session):
    question = db.query(Question).filter(Question.id == question_id).first()
    if not question:
        return jsonify({"detail": "题目不存在"}), 404
    if 'content' in data:
        question.content = data['content']
    if 'options' in data:
        question.options = data['options']
    if 'correct_answer' in data:
        question.correct_answer = data['correct_answer']
    if 'knowledge_id' in data:
        question.knowledge_id = data['knowledge_id']
    if 'difficulty' in data:
        question.difficulty = data['difficulty']
    if 'question_type' in data:
        question.question_type = data['question_type']
    db.commit()
    db.refresh(question)
    return jsonify({
        "id": question.id,
        "content": question.content,
        "options": question.options,
        "correct_answer": question.correct_answer,
        "knowledge_id": question.knowledge_id,
        "difficulty": question.difficulty,
        "question_type": question.question_type
    })

async def delete_question(question_id: int, db: Session):
    question = db.query(Question).filter(Question.id == question_id).first()
    if not question:
        return jsonify({"detail": "题目不存在"}), 404
    db.delete(question)
    db.commit()
    return jsonify({"message": "题目删除成功"})

def register_routes(app):
    @app.route('/api/question', methods=['GET'])
    async def flask_get_questions():
        knowledge_id = request.args.get('knowledge_id', type=int)
        difficulty = request.args.get('difficulty')
        db = next(get_db())
        try:
            return await get_questions(knowledge_id, difficulty, db)
        finally:
            db.close()
    
    @app.route('/api/question/<int:question_id>', methods=['GET'])
    async def flask_get_question(question_id):
        db = next(get_db())
        try:
            return await get_question(question_id, db)
        finally:
            db.close()
    
    @app.route('/api/question/ai-generate', methods=['POST'])
    async def flask_generate_question():
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({"detail": "未授权"}), 401
        token = token.split(' ')[1]
        current_user = get_current_user(token)
        if not current_user:
            return jsonify({"detail": "未授权"}), 401
        data = request.get_json()
        knowledge_id = data.get('knowledge_id')
        difficulty = data.get('difficulty')
        question_type = data.get('question_type')
        db = next(get_db())
        try:
            return await generate_question(knowledge_id, difficulty, question_type, db)
        finally:
            db.close()
    
    @app.route('/api/question', methods=['POST'])
    async def flask_create_question():
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({"detail": "未授权"}), 401
        token = token.split(' ')[1]
        current_user = get_current_user(token)
        if not current_user:
            return jsonify({"detail": "未授权"}), 401
        data = request.get_json()
        db = next(get_db())
        try:
            return await create_question(data, db)
        finally:
            db.close()
    
    @app.route('/api/question/<int:question_id>', methods=['PUT'])
    async def flask_update_question(question_id):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({"detail": "未授权"}), 401
        token = token.split(' ')[1]
        current_user = get_current_user(token)
        if not current_user:
            return jsonify({"detail": "未授权"}), 401
        data = request.get_json()
        db = next(get_db())
        try:
            return await update_question(question_id, data, db)
        finally:
            db.close()
    
    @app.route('/api/question/<int:question_id>', methods=['DELETE'])
    async def flask_delete_question(question_id):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({"detail": "未授权"}), 401
        token = token.split(' ')[1]
        current_user = get_current_user(token)
        if not current_user:
            return jsonify({"detail": "未授权"}), 401
        db = next(get_db())
        try:
            return await delete_question(question_id, db)
        finally:
            db.close()
