from flask import Blueprint, request, jsonify
from app.models.highlight import KnowledgeHighlight
from app.utils.database import SessionLocal
import time

highlight_bp = Blueprint('highlight', __name__)

@highlight_bp.route('/knowledge/highlight', methods=['POST'])
def create_highlight():
    """创建高亮笔记"""
    data = request.json
    db = SessionLocal()
    
    try:
        highlight = KnowledgeHighlight(
            knowledge_id=data['knowledge_id'],
            section_id=data.get('section_id'),
            highlight_id=data['highlight_id'],
            text=data['text'],
            note=data.get('note'),
            start_pos=data['start_pos'],
            end_pos=data['end_pos'],
            start_context=data.get('start_context'),
            end_context=data.get('end_context'),
            created_at=int(time.time())
        )
        
        db.add(highlight)
        db.commit()
        db.refresh(highlight)
        
        return jsonify({
            'id': highlight.id,
            'highlight_id': highlight.highlight_id,
            'message': '高亮创建成功'
        }), 201
    finally:
        db.close()

@highlight_bp.route('/knowledge/<int:knowledge_id>/highlights', methods=['GET'])
def get_highlights(knowledge_id):
    """获取知识点的所有高亮笔记"""
    db = SessionLocal()
    
    try:
        # 获取section_id参数
        section_id = request.args.get('section_id', type=int)
        
        query = db.query(KnowledgeHighlight).filter(
            KnowledgeHighlight.knowledge_id == knowledge_id
        )
        
        # 如果提供了section_id，添加过滤条件
        if section_id:
            query = query.filter(KnowledgeHighlight.section_id == section_id)
        
        highlights = query.all()
        
        return jsonify([{
            'id': h.id,
            'highlight_id': h.highlight_id,
            'text': h.text,
            'note': h.note,
            'start_pos': h.start_pos,
            'end_pos': h.end_pos,
            'start_context': h.start_context,
            'end_context': h.end_context,
            'created_at': h.created_at
        } for h in highlights]), 200
    finally:
        db.close()

@highlight_bp.route('/knowledge/highlight/<string:highlight_id>', methods=['PUT'])
def update_highlight(highlight_id):
    """更新高亮笔记"""
    data = request.json
    db = SessionLocal()
    
    try:
        highlight = db.query(KnowledgeHighlight).filter(
            KnowledgeHighlight.highlight_id == highlight_id
        ).first()
        
        if not highlight:
            return jsonify({'message': '高亮不存在'}), 404
        
        if 'note' in data:
            highlight.note = data['note']
        if 'start_pos' in data:
            highlight.start_pos = data['start_pos']
        if 'end_pos' in data:
            highlight.end_pos = data['end_pos']
        if 'start_context' in data:
            highlight.start_context = data['start_context']
        if 'end_context' in data:
            highlight.end_context = data['end_context']
        
        db.commit()
        db.refresh(highlight)
        
        return jsonify({
            'id': highlight.id,
            'highlight_id': highlight.highlight_id,
            'message': '高亮更新成功'
        }), 200
    finally:
        db.close()

@highlight_bp.route('/knowledge/highlight/<string:highlight_id>', methods=['DELETE'])
def delete_highlight(highlight_id):
    """删除高亮笔记"""
    db = SessionLocal()
    
    try:
        highlight = db.query(KnowledgeHighlight).filter(
            KnowledgeHighlight.highlight_id == highlight_id
        ).first()
        
        if not highlight:
            return jsonify({'message': '高亮不存在'}), 404
        
        db.delete(highlight)
        db.commit()
        
        return jsonify({'message': '高亮删除成功'}), 200
    finally:
        db.close()

def register_routes(app):
    app.register_blueprint(highlight_bp, url_prefix='/api')
