from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.utils.database import get_db
from app.utils.security import get_current_user
from app.models.user import User
from app.services.report_generator import generate_learning_report, generate_weak_points

router = APIRouter()

@router.get("/learning-report")
async def get_learning_report(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    report = generate_learning_report(current_user.id, db)
    return report

@router.get("/weak-points")
async def get_weak_points(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    weak_points = generate_weak_points(current_user.id, db)
    return weak_points
