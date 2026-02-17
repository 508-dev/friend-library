FROM python:3.12-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Collect static files
RUN python manage.py collectstatic --noinput

# Create media directory
RUN mkdir -p /app/media

EXPOSE 8000

# Run with gunicorn in production
CMD ["sh", "-c", "python manage.py migrate && python manage.py ensure_root_user && gunicorn stuff4friends.wsgi:application --bind 0.0.0.0:8000"]
