from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    attempts = relationship("ExamAttempt", back_populates="user")

class Question(Base):
    __tablename__ = "questions"
    
    id = Column(Integer, primary_key=True, index=True)
    topic = Column(String, nullable=False)  # Например: "101.1"
    question_type = Column(String, nullable=False)  # "single", "multiple", "text"
    text = Column(String, nullable=False)
    options = Column(JSON)  # Для multiple choice: [{"id": "A", "text": "..."}]
    correct_answer = Column(String, nullable=False)  # "A" или "A,C" или "lspci"
    explanation = Column(String)
    
    def get_correct_answers(self):
        return [ans.strip() for ans in self.correct_answer.split(",")]

class ExamAttempt(Base):
    __tablename__ = "exam_attempts"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    started_at = Column(DateTime, default=datetime.utcnow)
    finished_at = Column(DateTime)
    total_questions = Column(Integer)
    correct_answers = Column(Integer)
    score_percentage = Column(Float)
    is_passed = Column(Boolean)
    
    user = relationship("User", back_populates="attempts")
    answers = relationship("AttemptAnswer", back_populates="attempt")

class AttemptAnswer(Base):
    __tablename__ = "attempt_answers"
    
    id = Column(Integer, primary_key=True, index=True)
    attempt_id = Column(Integer, ForeignKey("exam_attempts.id"))
    question_id = Column(Integer, ForeignKey("questions.id"))
    user_answer = Column(String)
    is_correct = Column(Boolean)
    
    attempt = relationship("ExamAttempt", back_populates="answers")
    question = relationship("Question")
