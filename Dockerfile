# Use official Python runtime as base image
FROM python:3.11-slim-buster

# Set environment variables
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

# Set work directory and create app user
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first to leverage Docker cache
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project
COPY . .

# Create non-root user and switch to it
RUN useradd -m appuser && chown -R appuser:appuser /app
USER appuser

# Expose the port the app runs on
EXPOSE 5000

# Command to run the application
CMD ["quart", "run", "--host", "0.0.0.0", "--port", "5000"]