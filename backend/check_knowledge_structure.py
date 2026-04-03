import sys
sys.path.append('backend')
from app.utils.database import SessionLocal
from app.models.knowledge import KnowledgePoint

db = SessionLocal()
try:
    # 一级知识点
    print('一级知识点:')
    level1_points = db.query(KnowledgePoint).filter(KnowledgePoint.level == 1).order_by(KnowledgePoint.order).all()
    for p in level1_points:
        print(f'  {p.id}: {p.title} (order: {p.order})')
    
    # 二级知识点（第一个一级知识点的子节点）
    if level1_points:
        first_level1_id = level1_points[0].id
        print('\n二级知识点:')
        level2_points = db.query(KnowledgePoint).filter(
            KnowledgePoint.level == 2,
            KnowledgePoint.parent_id == first_level1_id
        ).order_by(KnowledgePoint.order).all()
        for p in level2_points:
            print(f'  {p.id}: {p.title} (parent: {p.parent_id}, order: {p.order})')
        
        # 三级知识点（二级知识点的子节点）
        if level2_points:
            level2_ids = [p.id for p in level2_points]
            print('\n三级知识点:')
            level3_points = db.query(KnowledgePoint).filter(
                KnowledgePoint.level == 3,
                KnowledgePoint.parent_id.in_(level2_ids)
            ).order_by(KnowledgePoint.order).all()
            for p in level3_points:
                print(f'  {p.id}: {p.title} (parent: {p.parent_id}, order: {p.order})')
finally:
    db.close()
