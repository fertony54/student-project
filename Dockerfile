# ─────────────────────────────────────────────────────────────
#  Dockerfile — Student Management API
#
#  The concept notes describe Docker as the way to "package the
#  application consistently and avoid server configuration issues."
#  This file is that idea made concrete: one image that runs the
#  same way on a laptop, in CI, and in production.
#
#  Build:  docker build -t student-api .
#  Run:    docker run -p 8000:8000 student-api
#  Docs:   http://localhost:8000/docs
# ─────────────────────────────────────────────────────────────

# Small, official Python base image
FROM python:3.11-slim

# Don't buffer stdout/stderr (logs appear immediately) and
# don't write .pyc files inside the container.
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

WORKDIR /app

# Install dependencies first so this layer is cached when only
# application code changes (faster rebuilds).
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Copy the application source
COPY . .

# Document the port the app listens on
EXPOSE 8000

# Start the API. Render/other platforms inject $PORT; default to 8000 locally.
CMD ["sh", "-c", "uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}"]
