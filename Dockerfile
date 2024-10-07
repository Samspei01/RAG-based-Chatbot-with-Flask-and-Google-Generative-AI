# Use the official Python image from the Docker Hub
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Upgrade pip to ensure we are using the latest version for Python 3.9
RUN python3.9 -m pip install --upgrade pip

# Upgrade setuptools and wheel to the latest versions
RUN python3.9 -m pip install --upgrade setuptools wheel

# Install Python dependencies
COPY requirements.txt ./
RUN python3.9 -m pip install --no-cache-dir -r requirements.txt

# Check pip version
RUN python3.9 -m pip --version

# Make port 5000 available to the world outside this container
EXPOSE 5000

# Define the command to run the application
CMD ["python3.9", "app.py"]