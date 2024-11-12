# Use the official Python image
FROM python:3.12

# Set the working directory in the container
WORKDIR /app

# Copy requirements.txt first to leverage Docker cache
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the project files to the container
COPY . .

# Set environment variables for Django
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Add ssh files with correct permissions (needed for deploying)
RUN mkdir /ssh && cp /app/deploy/ssh/* /ssh && chmod -R 600 /ssh