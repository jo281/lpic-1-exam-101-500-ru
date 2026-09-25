import React, { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import api from '../api/axios'

function Exam() {
  const [questions, setQuestions] = useState([])
  const [currentQuestionIndex, setCurrentQuestionIndex] = useState(0)
  const [answers, setAnswers] = useState({})
  const [timeLeft, setTimeLeft] = useState(30 * 60) // 30 минут
  const [loading, setLoading] = useState(true)
  const [submitting, setSubmitting] = useState(false)
  const navigate = useNavigate()

  useEffect(() => {
    loadQuestions()
  }, [])

  useEffect(() => {
    // Таймер
    const timer = setInterval(() => {
      setTimeLeft((prev) => {
        if (prev <= 1) {
          clearInterval(timer)
          handleSubmit()
          return 0
        }
        return prev - 1
      })
    }, 1000)

    return () => clearInterval(timer)
  }, [])

  const loadQuestions = async () => {
    try {
      const response = await api.get('/exam/start')
      setQuestions(response.data)
    } catch (err) {
      console.error('Ошибка загрузки вопросов:', err)
      alert('Ошибка загрузки вопросов')
      navigate('/dashboard')
    } finally {
      setLoading(false)
    }
  }

  const handleAnswerChange = (questionId, answer) => {
    setAnswers((prev) => ({
      ...prev,
      [questionId]: answer,
    }))
  }

  const handleOptionSelect = (questionId, optionId, isMultiple) => {
    const currentAnswer = answers[questionId] || ''
    
    if (isMultiple) {
      const selectedOptions = currentAnswer ? currentAnswer.split(',') : []
      const newOptions = selectedOptions.includes(optionId)
        ? selectedOptions.filter((id) => id !== optionId)
        : [...selectedOptions, optionId]
      handleAnswerChange(questionId, newOptions.join(','))
    } else {
      handleAnswerChange(questionId, optionId)
    }
  }

  const handleSubmit = async () => {
    if (submitting) return
    setSubmitting(true)

    try {
      const answersArray = Object.entries(answers).map(([questionId, answer]) => ({
        question_id: parseInt(questionId),
        answer: answer,
      }))

      const response = await api.post('/exam/submit', answersArray)
      navigate(`/results/${response.data.attempt_id}`)
    } catch (err) {
      console.error('Ошибка отправки ответов:', err)
      alert('Ошибка отправки ответов')
      setSubmitting(false)
    }
  }

  const formatTime = (seconds) => {
    const mins = Math.floor(seconds / 60)
    const secs = seconds % 60
    return `${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`
  }

  if (loading) {
    return <div className="container">Загрузка вопросов...</div>
  }

  const currentQuestion = questions[currentQuestionIndex]
  const progress = ((currentQuestionIndex + 1) / questions.length) * 100

  return (
    <div className="exam-container">
      <div className="exam-header">
        <div className="timer">{formatTime(timeLeft)}</div>
        <div className="progress-bar">
          <div className="progress-fill" style={{ width: `${progress}%` }}></div>
        </div>
        <div>
          Вопрос {currentQuestionIndex + 1} из {questions.length}
        </div>
      </div>

      <div className="question-card">
        <div className="question-topic">{currentQuestion.topic}</div>
        <div className="question-text">{currentQuestion.text}</div>

        {currentQuestion.question_type === 'single' && (
          <ul className="options-list">
            {currentQuestion.options.map((option) => (
              <li
                key={option.id}
                className={`option-item ${answers[currentQuestion.id] === option.id ? 'selected' : ''}`}
                onClick={() => handleOptionSelect(currentQuestion.id, option.id, false)}
              >
                <input
                  type="radio"
                  name={`question-${currentQuestion.id}`}
                  checked={answers[currentQuestion.id] === option.id}
                  onChange={() => {}}
                />
                {option.id}) {option.text}
              </li>
            ))}
          </ul>
        )}

        {currentQuestion.question_type === 'multiple' && (
          <>
            <p style={{ marginBottom: '15px', color: '#666', fontStyle: 'italic' }}>
              Выберите несколько правильных ответов
            </p>
            <ul className="options-list">
              {currentQuestion.options.map((option) => {
                const selectedOptions = (answers[currentQuestion.id] || '').split(',')
                return (
                  <li
                    key={option.id}
                    className={`option-item ${selectedOptions.includes(option.id) ? 'selected' : ''}`}
                    onClick={() => handleOptionSelect(currentQuestion.id, option.id, true)}
                  >
                    <input
                      type="checkbox"
                      checked={selectedOptions.includes(option.id)}
                      onChange={() => {}}
                    />
                    {option.id}) {option.text}
                  </li>
                )
              })}
            </ul>
          </>
        )}

        {currentQuestion.question_type === 'text' && (
          <input
            type="text"
            className="text-input"
            placeholder="Введите ваш ответ"
            value={answers[currentQuestion.id] || ''}
            onChange={(e) => handleAnswerChange(currentQuestion.id, e.target.value)}
          />
        )}
      </div>

      <div className="exam-navigation">
        <button
          className="btn-nav"
          onClick={() => setCurrentQuestionIndex((prev) => Math.max(0, prev - 1))}
          disabled={currentQuestionIndex === 0}
        >
          ← Назад
        </button>

        {currentQuestionIndex === questions.length - 1 ? (
          <button
            className="btn-nav"
            onClick={handleSubmit}
            disabled={submitting}
            style={{ background: '#4caf50' }}
          >
            {submitting ? 'Отправка...' : 'Завершить экзамен'}
          </button>
        ) : (
          <button
            className="btn-nav"
            onClick={() => setCurrentQuestionIndex((prev) => Math.min(questions.length - 1, prev + 1))}
          >
            Далее →
          </button>
        )}
      </div>
    </div>
  )
}

export default Exam
