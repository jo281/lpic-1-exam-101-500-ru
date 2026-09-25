import React, { useState, useEffect } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import api from '../api/axios'

function Results() {
  const { attemptId } = useParams()
  const [results, setResults] = useState(null)
  const [loading, setLoading] = useState(true)
  const navigate = useNavigate()

  useEffect(() => {
    loadResults()
  }, [attemptId])

  const loadResults = async () => {
    try {
      const response = await api.get(`/exam/attempts/${attemptId}`)
      setResults(response.data)
    } catch (err) {
      console.error('Ошибка загрузки результатов:', err)
      alert('Ошибка загрузки результатов')
      navigate('/dashboard')
    } finally {
      setLoading(false)
    }
  }

  if (loading) {
    return <div className="container">Загрузка результатов...</div>
  }

  if (!results) {
    return <div className="container">Результаты не найдены</div>
  }

  return (
    <div className="results-container">
      <div className={`results-header ${results.is_passed ? 'passed' : 'failed'}`}>
        <h1>{results.is_passed ? '✓ ЭКЗАМЕН СДАН' : '✗ ЭКЗАМЕН НЕ СДАН'}</h1>
        <div className={`score-display ${results.is_passed ? 'passed' : 'failed'}`}>
          {results.score_percentage.toFixed(1)}%
        </div>
        <p>
          Правильных ответов: {results.correct_answers} из {results.total_questions}
        </p>
        <p style={{ marginTop: '10px', color: '#666' }}>
          Проходной балл: 70%
        </p>
      </div>

      <div className="topic-breakdown">
        <h2>Результаты по темам</h2>
        {Object.entries(results.topic_breakdown).map(([topic, stats]) => (
          <div key={topic} className="topic-item">
            <div className="topic-name">Тема {topic}</div>
            <div className="topic-stats">
              <span>
                {stats.correct} / {stats.total}
              </span>
              <span
                className={`topic-percentage ${
                  stats.percentage >= 70 ? 'good' : stats.percentage >= 50 ? 'medium' : 'bad'
                }`}
              >
                {stats.percentage}%
              </span>
            </div>
          </div>
        ))}
      </div>

      <div className="detailed-results">
        <h2>Детальный разбор ответов</h2>
        {results.detailed_results.map((result, index) => (
          <div key={index} className={`result-item ${result.is_correct ? 'correct' : 'incorrect'}`}>
            <div className="result-question">
              Вопрос {index + 1} (Тема {result.topic}): {result.question_text}
            </div>
            
            {result.options && (
              <div style={{ marginTop: '10px' }}>
                {result.options.map((option) => (
                  <div
                    key={option.id}
                    style={{
                      padding: '8px',
                      margin: '5px 0',
                      background: option.id === result.correct_answer ? '#d4edda' : 
                                 option.id === result.user_answer && !result.is_correct ? '#f8d7da' : 'white',
                      borderRadius: '4px',
                      border: option.id === result.correct_answer ? '2px solid #4caf50' : '1px solid #e0e0e0'
                    }}
                  >
                    {option.id}) {option.text}
                    {option.id === result.correct_answer && ' ✓'}
                    {option.id === result.user_answer && !result.is_correct && ' ✗ (ваш ответ)'}
                  </div>
                ))}
              </div>
            )}

            {!result.options && (
              <div style={{ marginTop: '10px' }}>
                <div className="result-answer">
                  <strong>Правильный ответ:</strong> {result.correct_answer}
                </div>
                <div className="result-answer">
                  <strong>Ваш ответ:</strong> {result.user_answer || '(пусто)'}
                </div>
              </div>
            )}

            {result.explanation && (
              <div className="result-explanation">
                <strong>Объяснение:</strong> {result.explanation}
              </div>
            )}
          </div>
        ))}
      </div>

      <div style={{ textAlign: 'center', marginTop: '30px' }}>
        <button onClick={() => navigate('/dashboard')} className="btn-primary">
          Вернуться на главную
        </button>
      </div>
    </div>
  )
}

export default Results
