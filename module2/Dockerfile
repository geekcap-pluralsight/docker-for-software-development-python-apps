# Multi-stage Dockerfile for Python Flask application

# Stage 1: Test stage - Build environment with virtual environment and run tests
FROM python AS test-stage

WORKDIR /code

# Create virtual environment
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Activate the virtual environment
RUN . /opt/venv/bin/activate

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies in virtual environment
RUN pip install -r requirements.txt

# Copy application code
COPY src/ .

# Set the database host environment variable
ENV DATABASE_URL=sqlite:///:memory:

# Run tests
RUN python -m pytest tests_in_memory_database.py -v

# Stage 2: Production stage
FROM test-stage

WORKDIR /code

# Activate the virtual environment
RUN . /opt/venv/bin/activate

# Set environment variables
ENV FLASK_APP=app.py
ENV FLASK_ENV=production
ENV DATABASE_URL=mysql://root:password@host.docker.internal/coffees

# Run the application
CMD [ "python", "app.py" ]
