FROM python:3.11-slim

WORKDIR /app

# install system deps (penting untuk psycopg / build)
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# copy project
COPY src/backend /app

# install dependencies dari pyproject
RUN pip install --no-cache-dir -e .

EXPOSE 8000

# Tambahkan --reload dan --reload-dir agar uvicorn fokus mengawasi folder /app
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload", "--reload-dir", "/app"]