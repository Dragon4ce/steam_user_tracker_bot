FROM python:3.11-slim

# Отключаем буферизацию (полезно для логов)
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

WORKDIR /app

# Копируем зависимости и ставим их
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем весь код
COPY . .

# Запускаем uvicorn (важно: bot:app, а не bot.py)
CMD ["uvicorn", "bot:app", "--host", "0.0.0.0", "--port", "3000"]