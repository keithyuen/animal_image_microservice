# Use the official Python image from the Docker Hub
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file to the working directory
COPY requirements.txt .

# Install dependencies, including pytest
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code to the container
COPY ./app ./app
COPY ./tests ./tests

# Set PYTHONPATH to make the app module accessible
ENV PYTHONPATH=/app

# Expose port 80 to the outside world
EXPOSE 80

# Command to run the FastAPI application using Uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]
