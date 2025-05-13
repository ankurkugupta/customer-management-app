# Use Python 3.12 as base image
FROM python:3.12-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV VIRTUAL_ENV=/opt/venv
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        gcc \
        python3-dev \
        curl \
    && rm -rf /var/lib/apt/lists/*

# Create and activate virtual environment
RUN python -m venv $VIRTUAL_ENV

# Install Python dependencies
COPY requirements.txt .
RUN . $VIRTUAL_ENV/bin/activate && \
    pip install --no-cache-dir -r requirements.txt && \
    pip install --no-cache-dir gunicorn

# Copy only necessary project files
COPY manage.py .
COPY CustomerManagementApp/ CustomerManagementApp/
COPY customers/ customers/
COPY users/ users/
COPY templates/ templates/
COPY common/ common/

# Create necessary directories and set permissions
RUN mkdir -p logs static staticfiles   && \
    chmod -R 777 logs static staticfiles

# Create initialization script in /usr/local/bin
RUN echo '#!/bin/bash\n\
echo "Checking database..."\n\
cd /app\n\
if [ ! -s "db.sqlite3" ]; then\n\
    echo "Database does not exist or is empty. Creating new database..."\n\
    python manage.py makemigrations users\n\
    python manage.py makemigrations customers\n\
    python manage.py migrate \n\
    echo "Database created successfully."\n\
else\n\
    echo "Using existing database."\n\
fi\n\
' > /usr/local/bin/init-db.sh && chmod +x /usr/local/bin/init-db.sh

# Create a non-root user
RUN useradd -m appuser && chown -R appuser:appuser /app
USER appuser

# Expose port
EXPOSE 8000

# Run the application with Gunicorn
CMD ["gunicorn", "CustomerManagementApp.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "3", "--timeout", "120"] 