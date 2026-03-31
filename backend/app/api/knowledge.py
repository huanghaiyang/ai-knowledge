from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.models.knowledge import KnowledgePoint
from app.schemas.knowledge import KnowledgePointCreate, KnowledgePointResponse, KnowledgePointUpdate
from app.utils.database import get_db
from app.utils.security import get_current_user
from app.models.user import User

router = APIRouter()

@router.get("/", response_model=list[KnowledgePointResponse])
async def get_knowledge_points(db: Session = Depends(get_db)):
    knowledge_points = db.query(KnowledgePoint).all()
    return knowledge_points

@router.get("/{knowledge_id}", response_model=KnowledgePointResponse)
async def get_knowledge_point(knowledge_id: int, db: Session = Depends(get_db)):
    knowledge_point = db.query(KnowledgePoint).filter(KnowledgePoint.id == knowledge_id).first()
    if not knowledge_point:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="知识点不存在"
        )
    return knowledge_point

@router.post("/", response_model=KnowledgePointResponse)
async def create_knowledge_point(
    knowledge_point: KnowledgePointCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    new_knowledge_point = KnowledgePoint(**knowledge_point.model_dump())
    db.add(new_knowledge_point)
    db.commit()
    db.refresh(new_knowledge_point)
    return new_knowledge_point

@router.put("/{knowledge_id}", response_model=KnowledgePointResponse)
async def update_knowledge_point(
    knowledge_id: int,
    knowledge_point_update: KnowledgePointUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    knowledge_point = db.query(KnowledgePoint).filter(KnowledgePoint.id == knowledge_id).first()
    if not knowledge_point:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="知识点不存在"
        )
    for field, value in knowledge_point_update.model_dump(exclude_unset=True).items():
        setattr(knowledge_point, field, value)
    db.commit()
    db.refresh(knowledge_point)
    return knowledge_point

@router.delete("/{knowledge_id}")
async def delete_knowledge_point(
    knowledge_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    knowledge_point = db.query(KnowledgePoint).filter(KnowledgePoint.id == knowledge_id).first()
    if not knowledge_point:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="知识点不存在"
        )
    db.delete(knowledge_point)
    db.commit()
    return {"message": "知识点删除成功"}
