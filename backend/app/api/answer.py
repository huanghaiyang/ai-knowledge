from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.models.answer import Answer, UserAnswer
from app.schemas.answer import AnswerCreate, AnswerResponse, UserAnswerCreate, UserAnswerResponse
from app.utils.database import get_db
from app.utils.security import get_current_user
from app.models.user import User
from app.services.ai_grader import grade_answer

router = APIRouter()

@router.post("/user-answer", response_model=UserAnswerResponse)
async def submit_answer(
    user_answer: UserAnswerCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # 检查题目是否存在
    question = db.query(Answer.question).filter(Answer.question_id == user_answer.question_id).first()
    if not question:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="题目不存在"
        )
    
    # 自动批改
    is_correct, score, feedback = grade_answer(user_answer.question_id, user_answer.user_answer)
    
    # 保存用户答案
    new_user_answer = UserAnswer(
        user_id=current_user.id,
        question_id=user_answer.question_id,
        user_answer=user_answer.user_answer,
        is_correct=is_correct,
        score=score,
        feedback=feedback
    )
    db.add(new_user_answer)
    db.commit()
    db.refresh(new_user_answer)
    
    return new_user_answer

@router.get("/user-answers", response_model=list[UserAnswerResponse])
async def get_user_answers(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    user_answers = db.query(UserAnswer).filter(UserAnswer.user_id == current_user.id).all()
    return user_answers

@router.get("/user-answers/incorrect", response_model=list[UserAnswerResponse])
async def get_incorrect_answers(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    incorrect_answers = db.query(UserAnswer).filter(
        UserAnswer.user_id == current_user.id,
        UserAnswer.is_correct == False
    ).all()
    return incorrect_answers
