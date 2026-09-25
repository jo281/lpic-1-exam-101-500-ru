from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from datetime import datetime
from typing import List

from database import engine, get_db, Base
from models import User, Question, ExamAttempt, AttemptAnswer
from schemas import (
    UserCreate, UserResponse, Token, QuestionResponse,
    AnswerSubmission, ExamResult, AttemptSummary
)
from auth import (
    get_password_hash, verify_password, create_access_token,
    get_current_user
)
from exam_logic import get_random_questions, calculate_exam_results

# Создание таблиц
Base.metadata.create_all(bind=engine)

app = FastAPI(title="LPIC-1 Exam 101")

# CORS для frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============ AUTH ENDPOINTS ============

@app.post("/api/auth/register", response_model=UserResponse)
async def register(user: UserCreate, db: Session = Depends(get_db)):
    # Проверка существующего пользователя
    db_user = db.query(User).filter(User.email == user.email).first()
    if db_user:
        raise HTTPException(
            status_code=400,
            detail="Пользователь с таким email уже существует"
        )
    
    # Создание пользователя
    hashed_password = get_password_hash(user.password)
    db_user = User(email=user.email, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@app.post("/api/auth/login", response_model=Token)
async def login(user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == user.email).first()
    if not db_user or not verify_password(user.password, db_user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неверный email или пароль"
        )
    
    access_token = create_access_token(data={"sub": db_user.email})
    return {"access_token": access_token, "token_type": "bearer"}

# ============ EXAM ENDPOINTS ============

@app.get("/api/exam/start", response_model=List[QuestionResponse])
async def start_exam(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Начать экзамен - получить 20 случайных вопросов"""
    questions = get_random_questions(db, count=20)
    
    # Создать запись о попытке
    attempt = ExamAttempt(
        user_id=current_user.id,
        total_questions=len(questions)
    )
    db.add(attempt)
    db.commit()
    db.refresh(attempt)
    
    # Сохранить attempt_id в сессии (в реальном приложении использовать Redis)
    # Для простоты возвращаем его в ответе
    return questions

@app.post("/api/exam/submit", response_model=ExamResult)
async def submit_exam(
    answers: List[AnswerSubmission],
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Отправить ответы на экзамен"""
    # Найти последнюю попытку пользователя
    attempt = db.query(ExamAttempt).filter(
        ExamAttempt.user_id == current_user.id,
        ExamAttempt.finished_at == None
    ).order_by(ExamAttempt.started_at.desc()).first()
    
    if not attempt:
        raise HTTPException(status_code=404, detail="Активная попытка не найдена")
    
    # Обработка ответов
    correct_count = 0
    for answer_data in answers:
        question = db.query(Question).filter(Question.id == answer_data.question_id).first()
        if not question:
            continue
        
        # Проверка правильности ответа
        correct_answers = question.get_correct_answers()
        user_answers = [ans.strip() for ans in answer_data.answer.split(",")]
        
        is_correct = set(correct_answers) == set(user_answers)
        if is_correct:
            correct_count += 1
        
        # Сохранить ответ
        attempt_answer = AttemptAnswer(
            attempt_id=attempt.id,
            question_id=answer_data.question_id,
            user_answer=answer_data.answer,
            is_correct=is_correct
        )
        db.add(attempt_answer)
    
    # Обновить попытку
    attempt.finished_at = datetime.utcnow()
    attempt.correct_answers = correct_count
    attempt.score_percentage = (correct_count / attempt.total_questions) * 100
    attempt.is_passed = attempt.score_percentage >= 70  # Проходной балл 70%
    
    db.commit()
    
    # Вернуть детальные результаты
    return calculate_exam_results(db, attempt.id)

@app.get("/api/exam/attempts", response_model=List[AttemptSummary])
async def get_attempts(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Получить историю попыток"""
    attempts = db.query(ExamAttempt).filter(
        ExamAttempt.user_id == current_user.id,
        ExamAttempt.finished_at != None
    ).order_by(ExamAttempt.started_at.desc()).all()
    
    return attempts

@app.get("/api/exam/attempts/{attempt_id}", response_model=ExamResult)
async def get_attempt_details(
    attempt_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Получить детали конкретной попытки"""
    attempt = db.query(ExamAttempt).filter(
        ExamAttempt.id == attempt_id,
        ExamAttempt.user_id == current_user.id
    ).first()
    
    if not attempt:
        raise HTTPException(status_code=404, detail="Попытка не найдена")
    
    return calculate_exam_results(db, attempt_id)

# ============ ADMIN ENDPOINTS (для добавления вопросов) ============

@app.post("/api/admin/questions")
async def add_question(
    question_data: dict,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Добавить новый вопрос (для администратора)"""
    question = Question(
        topic=question_data["topic"],
        question_type=question_data["question_type"],
        text=question_data["text"],
        options=question_data.get("options"),
        correct_answer=question_data["correct_answer"],
        explanation=question_data.get("explanation", "")
    )
    db.add(question)
    db.commit()
    return {"message": "Вопрос добавлен", "id": question.id}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
