from flask import request, jsonify
from sqlalchemy.orm import Session
from app.models.knowledge import KnowledgePoint
from app.utils.database import get_db
from app.utils.security import get_current_user
from app.utils.validators import KnowledgeValidator, UserValidator

async def get_knowledge_points(db: Session):
    knowledge_points = db.query(KnowledgePoint).all()
    return jsonify([
        {
            "id": kp.id,
            "title": kp.title,
            "description": kp.description,
            "difficulty": kp.difficulty,
            "category": kp.category
        } for kp in knowledge_points
    ])

async def get_knowledge_point(knowledge_id: int, db: Session):
    knowledge_point = db.query(KnowledgePoint).filter(KnowledgePoint.id == knowledge_id).first()
    if not knowledge_point:
        return jsonify({"detail": "知识点不存在"}), 404
    return jsonify({
        "id": knowledge_point.id,
        "title": knowledge_point.title,
        "description": knowledge_point.description,
        "difficulty": knowledge_point.difficulty,
        "category": knowledge_point.category
    })

async def create_knowledge_point(data: dict, db: Session):
    # 清理和验证输入
    title = UserValidator.sanitize_input(data.get('title', ''))
    description = UserValidator.sanitize_input(data.get('description', ''))
    difficulty = data.get('difficulty')
    category = data.get('category')
    
    # 验证知识点标题
    is_valid, message = KnowledgeValidator.validate_title(title)
    if not is_valid:
        return jsonify({"detail": message}), 400
    
    # 验证知识点描述
    is_valid, message = KnowledgeValidator.validate_description(description)
    if not is_valid:
        return jsonify({"detail": message}), 400
    
    new_knowledge_point = KnowledgePoint(
        title=title,
        description=description,
        difficulty=difficulty,
        category=category
    )
    db.add(new_knowledge_point)
    db.commit()
    db.refresh(new_knowledge_point)
    return jsonify({
        "id": new_knowledge_point.id,
        "title": new_knowledge_point.title,
        "description": new_knowledge_point.description,
        "difficulty": new_knowledge_point.difficulty,
        "category": new_knowledge_point.category
    })

async def update_knowledge_point(knowledge_id: int, data: dict, db: Session):
    knowledge_point = db.query(KnowledgePoint).filter(KnowledgePoint.id == knowledge_id).first()
    if not knowledge_point:
        return jsonify({"detail": "知识点不存在"}), 404
    if 'title' in data:
        knowledge_point.title = data['title']
    if 'description' in data:
        knowledge_point.description = data['description']
    if 'difficulty' in data:
        knowledge_point.difficulty = data['difficulty']
    if 'category' in data:
        knowledge_point.category = data['category']
    db.commit()
    db.refresh(knowledge_point)
    return jsonify({
        "id": knowledge_point.id,
        "title": knowledge_point.title,
        "description": knowledge_point.description,
        "difficulty": knowledge_point.difficulty,
        "category": knowledge_point.category
    })

async def delete_knowledge_point(knowledge_id: int, db: Session):
    knowledge_point = db.query(KnowledgePoint).filter(KnowledgePoint.id == knowledge_id).first()
    if not knowledge_point:
        return jsonify({"detail": "知识点不存在"}), 404
    db.delete(knowledge_point)
    db.commit()
    return jsonify({"message": "知识点删除成功"})

def register_routes(app):
    @app.route('/api/knowledge', methods=['GET'])
    async def flask_get_knowledge_points():
        db = next(get_db())
        return await get_knowledge_points(db)
    
    @app.route('/api/knowledge/<int:knowledge_id>', methods=['GET'])
    async def flask_get_knowledge_point(knowledge_id):
        db = next(get_db())
        return await get_knowledge_point(knowledge_id, db)
    
    @app.route('/api/knowledge', methods=['POST'])
    async def flask_create_knowledge_point():
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({"detail": "未授权"}), 401
        token = token.split(' ')[1]
        current_user = get_current_user(token)
        if not current_user:
            return jsonify({"detail": "未授权"}), 401
        data = request.get_json()
        db = next(get_db())
        return await create_knowledge_point(data, db)
    
    @app.route('/api/knowledge/<int:knowledge_id>', methods=['PUT'])
    async def flask_update_knowledge_point(knowledge_id):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({"detail": "未授权"}), 401
        token = token.split(' ')[1]
        current_user = get_current_user(token)
        if not current_user:
            return jsonify({"detail": "未授权"}), 401
        data = request.get_json()
        db = next(get_db())
        return await update_knowledge_point(knowledge_id, data, db)
    
    @app.route('/api/knowledge/<int:knowledge_id>', methods=['DELETE'])
    async def flask_delete_knowledge_point(knowledge_id):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({"detail": "未授权"}), 401
        token = token.split(' ')[1]
        current_user = get_current_user(token)
        if not current_user:
            return jsonify({"detail": "未授权"}), 401
        db = next(get_db())
        return await delete_knowledge_point(knowledge_id, db)
