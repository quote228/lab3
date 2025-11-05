FROM python:3.9-slim

# Устанавливаем зависимости для tkinter
RUN apt-get update && apt-get install -y \
    python3-tk \
    tk-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app/ ./app/
COPY tests/ ./tests/

# Запускаем без GUI (тестовый режим)
CMD ["python", "-c", "from app.calculator import MortgageCalculator; calc = MortgageCalculator(1000000, 7.5, 10); print(f'✅ Docker образ работает! Ежемесячный платеж: {calc.calculate_monthly_payment()} руб.')"]