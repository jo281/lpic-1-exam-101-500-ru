import React, { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import api from '../api/axios'

function Dashboard({ onLogout }) {
  const [attempts, setAttempts] = useState([])
  const [loading, setLoading] = useState(true)
  const navigate = useNavigate()

  useEffect(() => {
    loadAttempts()
  }, [])

  const loadAttempts = async () => {
    try {
      const response = await api.get('/exam/attempts')
      setAttempts(response.data)
    } catch (err) {
      console.error('Ошибка загрузки истории:', err)
    } finally {
      setLoading(false)
    }
  }

  const handleStartExam = async () => {
    navigate('/exam')
  }

  const handleViewResults = (attemptId) => {
    navigate(`/results/${attemptId}`)
  }

  return (
    <div className="dashboard">
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '30px' }}>
        <h1>LPIC-1 Exam 101</h1>
        <button onClick={onLogout} className="btn-secondary">Выйти</button>
      </div>

      <div className="dashboard-actions">
        <button onClick={handleStartExam} className="btn-primary">
          Начать экзамен
        </button>
      </div>

      <div className="attempts-section">
        <h2>История попыток</h2>
        {loading ? (
          <p>Загрузка...</p>
        ) : attempts.length === 0 ? (
          <p>Вы еще не проходили экзамен</p>
        ) : (
          attempts.map((attempt) => (
            <div
              key={attempt.id}
              className="attempt-card"
              onClick={() => handleViewResults(attempt.id)}
            >
              <div className="attempt-header">
                <div>
                  <div className="attempt-date">
                    {new Date(attempt.started_at).toLocaleString('ru-RU')}
                  </div>
                </div>
                <div className={`attempt-score ${attempt.is_passed ? 'passed' : 'failed'}`}>
                  {attempt.score_percentage.toFixed(1)}%
                </div>
              </div>
              <div>
                Правильных ответов: {attempt.correct_answers} из {attempt.total_questions}
              </div>
              <div style={{ marginTop: '10px', color: attempt.is_passed ? '#4caf50' : '#f44336', fontWeight: '600' }}>
                {attempt.is_passed ? '✓ СДАНО' : '✗ НЕ СДАНО'}
              </div>
            </div>
          ))
        )}
      </div>
    </div>
  )
}

export default Dashboard
