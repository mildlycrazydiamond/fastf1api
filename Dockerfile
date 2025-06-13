FROM python:3.11-slim

# Set working directory
WORKDIR /code

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Create app directory and copy code
COPY ./app ./app

# Create cache directory for Fast F1
RUN mkdir -p cache

# Expose port
EXPOSE 8000

# Run the application with the new package structure
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]