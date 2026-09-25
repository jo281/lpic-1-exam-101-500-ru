from sqlalchemy.orm import Session
from models import Question, ExamAttempt, AttemptAnswer
from datetime import datetime
from typing import List, Dict
import random

def get_random_questions(db: Session, count: int = 20) -> List[Question]:
    """Получить случайные вопросы из базы"""
    all_questions = db.query(Question).all()
    if len(all_questions) < count:
        return all_questions
    return random.sample(all_questions, count)

def calculate_exam_results(db: Session, attempt_id: int) -> Dict:
    """Подсчитать результаты экзамена"""
    attempt = db.query(ExamAttempt).filter(ExamAttempt.id == attempt_id).first()
    answers = db.query(AttemptAnswer).filter(AttemptAnswer.attempt_id == attempt_id).all()
    
    # Подсчет по темам
    topic_stats = {}
    detailed_results = []
    
    for answer in answers:
        question = db.query(Question).filter(Question.id == answer.question_id).first()
        topic = question.topic
        
        if topic not in topic_stats:
            topic_stats[topic] = {"total": 0, "correct": 0}
        
        topic_stats[topic]["total"] += 1
        if answer.is_correct:
            topic_stats[topic]["correct"] += 1
        
        detailed_results.append({
            "question_id": question.id,
            "question_text": question.text,
            "question_type": question.question_type,
            "options": question.options,
            "correct_answer": question.correct_answer,
            "user_answer": answer.user_answer,
            "is_correct": answer.is_correct,
            "explanation": question.explanation,
            "topic": topic
        })
    
    # Подсчет процентов по темам
    topic_breakdown = {}
    for topic, stats in topic_stats.items():
        percentage = (stats["correct"] / stats["total"] * 100) if stats["total"] > 0 else 0
        topic_breakdown[topic] = {
            "total": stats["total"],
            "correct": stats["correct"],
            "percentage": round(percentage, 1)
        }
    
    return {
        "attempt_id": attempt.id,
        "total_questions": attempt.total_questions,
        "correct_answers": attempt.correct_answers,
        "score_percentage": attempt.score_percentage,
        "is_passed": attempt.is_passed,
        "topic_breakdown": topic_breakdown,
        "detailed_results": detailed_results
    }
