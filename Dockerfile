FROM python:3.13-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create necessary directories
RUN mkdir -p user_files exports cache reports

# Create sample data files
RUN echo "This is a sample report." > reports/sample.txt && \
    echo "This is a sample app.py file." > user_files/app.py && \
    echo "This is config file." > user_files/config.py && \
    echo "This is .env file." > user_files/.env

# Expose port 5000
EXPOSE 5000

# Run the application
CMD ["python", "app.py"]