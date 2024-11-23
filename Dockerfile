# Use an official Python runtime as the base image
FROM python:3.13-slim

# Set the working directory in the container
WORKDIR /app

# Install system-level dependencies (for PostgreSQL and general build tools)
RUN apt-get update && apt-get install -y \
    libpq-dev gcc curl && \
    apt-get clean

# Install Poetry
RUN curl -sSL https://install.python-poetry.org | python3 - && \
    ln -s /root/.local/bin/poetry /usr/local/bin/poetry

# Copy project files into the container
COPY . /app

# Configure Poetry to not create virtual environments (dependencies install globally in the container)
RUN poetry config virtualenvs.create false

# Install Python dependencies using Poetry
RUN poetry install --no-root --no-dev

# Collect static files for Django
RUN python manage.py collectstatic --noinput

# Expose port 8000 (default Django port)
EXPOSE 8000

# Set the default command to run the app with Gunicorn
CMD ["poetry", "run", "gunicorn", "--bind", "0.0.0.0:8000", "epiclang.wsgi:application"]
