# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the current directory contents into the container
COPY . /app

# Install dependencies from the requirements file
RUN pip install --no-cache-dir -r requirements.txt

# Expose port 8000 (default port for FastAPI)
EXPOSE 8000

# Set environment variable to avoid Python buffering
ENV PYTHONUNBUFFERED 1

# Command to run the app
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
