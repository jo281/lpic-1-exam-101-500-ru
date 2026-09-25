#!/bin/bash
set -e

# Ждём, пока PostgreSQL станет доступен
echo "⏳ Ожидание PostgreSQL..."
until python -c "
import os
from sqlalchemy import create_engine, text
engine = create_engine(os.getenv('DATABASE_URL'))
with engine.connect() as conn:
    conn.execute(text('SELECT 1'))
print('ok')
" 2>/dev/null | grep -q "ok"; do
    echo "  PostgreSQL ещё не готов, ждём..."
    sleep 2
done
echo "✅ PostgreSQL доступен."

# Создаём таблицы
echo "📦 Инициализация схемы БД..."
python -c "
from database import engine, Base
Base.metadata.create_all(bind=engine)
print('✅ Таблицы созданы.')
"

# Сидируем вопросы, если база пустая
echo "📚 Проверка наличия вопросов..."
python seed_questions.py

echo "🚀 Запускаю FastAPI..."
exec uvicorn main:app --host 0.0.0.0 --port 8000
