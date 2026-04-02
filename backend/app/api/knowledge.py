from flask import request, jsonify
from sqlalchemy.orm import Session
from app.models.knowledge import KnowledgePoint
from app.models.content import KnowledgeContent
from app.utils.database import get_db
from app.utils.security import get_current_user
from app.utils.validators import KnowledgeValidator, UserValidator
from app.services.vector_service import VectorService

async def get_knowledge_points(db: Session):
    knowledge_points = db.query(KnowledgePoint).all()
    return jsonify([
        {
            "id": kp.id,
            "title": kp.title,
            "description": kp.description,
            "parent_id": kp.parent_id,
            "level": kp.level
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
        "parent_id": knowledge_point.parent_id,
        "level": knowledge_point.level
    })

async def create_knowledge_point(data: dict, db: Session):
    # 清理和验证输入
    title = UserValidator.sanitize_input(data.get('title', ''))
    description = UserValidator.sanitize_input(data.get('description', ''))
    parent_id = data.get('parent_id')
    level = data.get('level', 1)
    
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
        parent_id=parent_id,
        level=level
    )
    db.add(new_knowledge_point)
    db.commit()
    db.refresh(new_knowledge_point)
    return jsonify({
        "id": new_knowledge_point.id,
        "title": new_knowledge_point.title,
        "description": new_knowledge_point.description,
        "parent_id": new_knowledge_point.parent_id,
        "level": new_knowledge_point.level
    })

async def update_knowledge_point(knowledge_id: int, data: dict, db: Session):
    knowledge_point = db.query(KnowledgePoint).filter(KnowledgePoint.id == knowledge_id).first()
    if not knowledge_point:
        return jsonify({"detail": "知识点不存在"}), 404
    if 'title' in data:
        knowledge_point.title = data['title']
    if 'description' in data:
        knowledge_point.description = data['description']
    if 'parent_id' in data:
        knowledge_point.parent_id = data['parent_id']
    if 'level' in data:
        knowledge_point.level = data['level']
    db.commit()
    db.refresh(knowledge_point)
    return jsonify({
        "id": knowledge_point.id,
        "title": knowledge_point.title,
        "description": knowledge_point.description,
        "parent_id": knowledge_point.parent_id,
        "level": knowledge_point.level
    })

async def delete_knowledge_point(knowledge_id: int, db: Session):
    knowledge_point = db.query(KnowledgePoint).filter(KnowledgePoint.id == knowledge_id).first()
    if not knowledge_point:
        return jsonify({"detail": "知识点不存在"}), 404
    db.delete(knowledge_point)
    db.commit()
    return jsonify({"message": "知识点删除成功"})

async def search_knowledge(query: str):
    """搜索相似的知识点"""
    if not query:
        return jsonify({"detail": "搜索关键词不能为空"}), 400
    
    results = VectorService.search_similar_knowledge(query)
    return jsonify(results)

async def update_embeddings():
    """更新所有知识点的嵌入向量"""
    result = VectorService.update_knowledge_embeddings()
    return jsonify({"message": result})

async def init_vector_store():
    """初始化向量存储"""
    # 由于没有pgvector扩展，暂时返回成功
    return jsonify({"message": "向量存储初始化完成（模拟）"})

async def get_knowledge_content(knowledge_id: int, db: Session):
    """获取知识点的章节内容"""
    knowledge_point = db.query(KnowledgePoint).filter(KnowledgePoint.id == knowledge_id).first()
    if not knowledge_point:
        return jsonify({"detail": "知识点不存在"}), 404
    
    content_sections = db.query(KnowledgeContent).filter(
        KnowledgeContent.knowledge_id == knowledge_id
    ).order_by(KnowledgeContent.order).all()
    
    return jsonify({
        "knowledge_id": knowledge_point.id,
        "knowledge_title": knowledge_point.title,
        "knowledge_description": knowledge_point.description,
        "content_sections": [
            {
                "id": section.id,
                "section_title": section.section_title,
                "content": section.content,
                "order": section.order
            }
            for section in content_sections
        ]
    })

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
    
    @app.route('/api/knowledge/search', methods=['GET'])
    async def flask_search_knowledge():
        query = request.args.get('q', '')
        print(f"查询参数: {query}")
        return await search_knowledge(query)
    
    @app.route('/api/knowledge/embeddings', methods=['POST'])
    async def flask_update_embeddings():
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({"detail": "未授权"}), 401
        token = token.split(' ')[1]
        current_user = get_current_user(token)
        if not current_user:
            return jsonify({"detail": "未授权"}), 401
        return await update_embeddings()
    
    @app.route('/api/knowledge/vector-store', methods=['POST'])
    async def flask_init_vector_store():
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({"detail": "未授权"}), 401
        token = token.split(' ')[1]
        current_user = get_current_user(token)
        if not current_user:
            return jsonify({"detail": "未授权"}), 401
        return await init_vector_store()
    
    @app.route('/api/knowledge/<int:knowledge_id>/content', methods=['GET'])
    async def flask_get_knowledge_content(knowledge_id):
        db = next(get_db())
        return await get_knowledge_content(knowledge_id, db)
