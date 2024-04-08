# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends gcc libpq-dev && rm -rf /var/lib/apt/lists/*

# Set the GOOGLE_APPLICATION_CREDENTIALS environment variable
ARG GOOGLE_APPLICATION_CREDENTIALS
ENV GOOGLE_APPLICATION_CREDENTIALS=${GOOGLE_APPLICATION_CREDENTIALS}

# Continue with your Dockerfile steps


# Install dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

COPY docusign_private_key.pem /app/docusign_private_key.pem


# Copy the current directory contents into the container at /app
COPY . /app/

# Run Django collectstatic
RUN python manage.py collectstatic --noinput

# Run the application
CMD gunicorn toph.wsgi:application --bind 0.0.0.0:$PORT
