# syntax=docker/dockerfile:1
FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

WORKDIR /app/src/main/raposo_emporio
CMD ["python", "app.py"]