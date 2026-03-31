from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from app.models.question import Question
from app.schemas.question import QuestionCreate, QuestionResponse, QuestionUpdate
from app.utils.database import get_db
from app.utils.security import get_current_user
from app.models.user import User
from app.services.ai_question_generator import generate_ai_question

router = APIRouter()

@router.get("/", response_model=list[QuestionResponse])
async def get_questions(
    knowledge_id: int = Query(None, description="知识点ID"),
    difficulty: str = Query(None, description="难度级别"),
    db: Session = Depends(get_db)
):
    query = db.query(Question)
    if knowledge_id:
        query = query.filter(Question.knowledge_id == knowledge_id)
    if difficulty:
        query = query.filter(Question.difficulty == difficulty)
    questions = query.all()
    return questions

@router.get("/{question_id}", response_model=QuestionResponse)
async def get_question(question_id: int, db: Session = Depends(get_db)):
    question = db.query(Question).filter(Question.id == question_id).first()
    if not question:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="题目不存在"
        )
    return question

@router.post("/ai-generate")
async def generate_question(
    knowledge_id: int,
    difficulty: str,
    question_type: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # 使用AI生成题目
    question_data = generate_ai_question(knowledge_id, difficulty, question_type)
    new_question = Question(**question_data)
    db.add(new_question)
    db.commit()
    db.refresh(new_question)
    return new_question

@router.post("/", response_model=QuestionResponse)
async def create_question(
    question: QuestionCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    new_question = Question(**question.model_dump())
    db.add(new_question)
    db.commit()
    db.refresh(new_question)
    return new_question

@router.put("/{question_id}", response_model=QuestionResponse)
async def update_question(
    question_id: int,
    question_update: QuestionUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    question = db.query(Question).filter(Question.id == question_id).first()
    if not question:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="题目不存在"
        )
    for field, value in question_update.model_dump(exclude_unset=True).items():
        setattr(question, field, value)
    db.commit()
    db.refresh(question)
    return question

@router.delete("/{question_id}")
async def delete_question(
    question_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    question = db.query(Question).filter(Question.id == question_id).first()
    if not question:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="题目不存在"
        )
    db.delete(question)
    db.commit()
    return {"message": "题目删除成功"}
