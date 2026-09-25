FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
  PYTHONUNBUFFERED=1 \
  PORT=5555

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip \
  && pip install --no-cache-dir -r requirements.txt

COPY app.py .

EXPOSE 5555

CMD ["gunicorn", "--bind", "0.0.0.0:5555", "--workers", "2", "--access-logfile", "-", "app:app"]