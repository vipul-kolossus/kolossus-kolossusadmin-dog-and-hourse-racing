# Stage 1: Build React frontend
FROM node:18-alpine AS frontend-builder
WORKDIR /frontend
COPY frontend/package.json ./
RUN npm install --legacy-peer-deps
COPY frontend/ ./
RUN CI=false npm run build

# Stage 2: Django backend
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY backend/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend source
COPY backend/ ./

# Copy React build into Django static files directory
RUN mkdir -p static/react
COPY --from=frontend-builder /frontend/build/ ./static/react/

# Fix the template to reference correct static files
RUN python -c "
import os, glob

# Find the JS and CSS chunks in React build
build_dir = 'static/react/static'
js_files = glob.glob(os.path.join(build_dir, 'js', 'main.*.js'))
css_files = glob.glob(os.path.join(build_dir, 'css', 'main.*.css'))

js_file = os.path.basename(js_files[0]) if js_files else 'main.js'
css_file = os.path.basename(css_files[0]) if css_files else 'main.css'

template = open('templates/index.html').read()
template = template.replace('react/static/css/main.css', f'react/static/css/{css_file}')
template = template.replace('react/static/js/main.js', f'react/static/js/{js_file}')
open('templates/index.html', 'w').write(template)
print(f'Template updated: js={js_file}, css={css_file}')
"

# Run migrations and seed data
RUN python manage.py makemigrations --noinput && \
    python manage.py migrate --noinput && \
    python manage.py seed_data && \
    python manage.py collectstatic --noinput

EXPOSE 8000

CMD ["gunicorn", "racing_project.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "2", "--timeout", "120"]
