# Use official light-weight Python image
FROM python:3.11-slim

# Set working directory inside the container
WORKDIR /app

#Copy requirements for dependencies caching
COPY requirements.txt .

# Set Labels
LABEL org.opencontainers.image.title="Scalable Containerized FastAPI App"
LABEL org.opencontainers.image.description="Simple FastAPI application to learn API foundations and how to develop a project which also integrates a database for permanent data storage."
LABEL org.opencontainers.image.version="2.1.0"

# Install python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY ./app ./app

# Create directory for shared database
RUN mkdir -p /app/data

# Expose port 8000 (FastAPI default)
EXPOSE 8000

# Start application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
        