# Use a multi-architecture base image
FROM python:3.12.4-slim as base

# Copy the application code
COPY . /app/
# Install dependencies
COPY requirements.txt /app/

# Set the working directory
WORKDIR /app

RUN pip3 install --no-cache-dir -r requirements.txt
# Expose the application port
EXPOSE 8080

# Command to run the application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]
