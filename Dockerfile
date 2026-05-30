# Use an official, optimized Python runtime as a parent image
FROM python:3.12-slim

# Set system environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PORT=8000

# Set working directory inside the container
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    shared-mime-info \
    mime-support \
    && rm -rf /var/lib/apt/lists/*

# Install python dependencies first to leverage Docker layer caching
COPY requirements.txt /app/
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . /app/

# Create a non-root user and group for security
RUN groupadd -r appuser && useradd -r -g appuser appuser \
    && chown -R appuser:appuser /app

# Make the entrypoint script executable
RUN chmod +x /app/entrypoint.sh

# Switch to the non-root user
USER appuser

# Run collectstatic during build so static files are packaged into the image
RUN python manage.py collectstatic --noinput --clear

# Expose the default port (Railway will override this automatically)
EXPOSE 8000

# Use the entrypoint script to handle migrations and start Gunicorn
ENTRYPOINT ["/app/entrypoint.sh"]
