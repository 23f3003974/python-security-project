# Use a small Python base
FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Copy your requirements and install them
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Simple command to run
CMD ["python", "--version"]
