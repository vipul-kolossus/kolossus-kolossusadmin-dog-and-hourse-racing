# Stage 1: Build React frontend
FROM node:18-alpine AS frontend-builder
WORKDIR /frontend
COPY frontend/package.json ./
RUN npm install --legacy-peer-deps
COPY frontend/ ./
ENV PUBLIC_URL=/static/react
RUN CI=false npm run build

# Stage 2: Django backend
FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

COPY backend/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY backend/ ./

RUN mkdir -p static/react
COPY --from=frontend-builder /frontend/build/ ./static/react/

RUN python manage.py makemigrations --noinput && \
    python manage.py migrate --noinput && \
    python manage.py seed_data && \
    python manage.py collectstatic --noinput

EXPOSE 8000

CMD ["gunicorn", "racing_project.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "2", "--timeout", "120"]
