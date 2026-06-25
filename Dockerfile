FROM python:3.11-slim

WORKDIR /app

RUN pip install --no-cache-dir uv

COPY backend/requirements.txt ./
RUN uv pip install --system --no-cache -r requirements.txt

COPY backend/ ./

RUN mkdir -p static
COPY frontend/index.html ./static/index.html

RUN python manage.py collectstatic --noinput

COPY entrypoint.sh ./entrypoint.sh
RUN chmod +x ./entrypoint.sh

EXPOSE 8000

CMD ["./entrypoint.sh"]
