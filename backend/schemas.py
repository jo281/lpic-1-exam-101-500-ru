from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional, List

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: int
    email: str
    created_at: datetime
    
    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class QuestionResponse(BaseModel):
    id: int
    topic: str
    question_type: str
    text: str
    options: Optional[List[dict]]
    
    class Config:
        from_attributes = True

class AnswerSubmission(BaseModel):
    question_id: int
    answer: str

class ExamResult(BaseModel):
    attempt_id: int
    total_questions: int
    correct_answers: int
    score_percentage: float
    is_passed: bool
    topic_breakdown: dict
    detailed_results: List[dict]

class AttemptSummary(BaseModel):
    id: int
    started_at: datetime
    finished_at: Optional[datetime]
    total_questions: int
    correct_answers: int
    score_percentage: float
    is_passed: bool
    
    class Config:
        from_attributes = True
