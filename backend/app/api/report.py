from flask import request, jsonify
from sqlalchemy.orm import Session
from app.utils.database import get_db
from app.utils.security import get_current_user
from app.services.report_generator import generate_learning_report, generate_weak_points

async def get_learning_report(current_user_id: int, db: Session):
    report = generate_learning_report(current_user_id, db)
    return jsonify(report)

async def get_weak_points(current_user_id: int, db: Session):
    weak_points = generate_weak_points(current_user_id, db)
    return jsonify(weak_points)

def register_routes(app):
    @app.route('/api/report/learning-report', methods=['GET'])
    async def flask_get_learning_report():
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({"detail": "未授权"}), 401
        token = token.split(' ')[1]
        current_user = get_current_user(token)
        if not current_user:
            return jsonify({"detail": "未授权"}), 401
        db = next(get_db())
        return await get_learning_report(current_user.id, db)
    
    @app.route('/api/report/weak-points', methods=['GET'])
    async def flask_get_weak_points():
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({"detail": "未授权"}), 401
        token = token.split(' ')[1]
        current_user = get_current_user(token)
        if not current_user:
            return jsonify({"detail": "未授权"}), 401
        db = next(get_db())
        return await get_weak_points(current_user.id, db)
