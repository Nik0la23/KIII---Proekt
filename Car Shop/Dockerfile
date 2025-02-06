FROM python:3.9-slim

WORKDIR /app

# Copy requirements first to leverage Docker cache
COPY requirements.txt .

# Install dependencies
RUN pip install -r requirements.txt

# Copy the rest of the application
COPY . .

# Expose the application's port
EXPOSE 5000

# Set environment variable for Flask
ENV FLASK_APP=app.py

# Command to run the application
CMD ["python", "app.py"]
