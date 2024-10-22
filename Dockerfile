# Use official Python image
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose port 80 for Flask
EXPOSE 80

# Set environment variables
ENV FLASK_ENV=development
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_RUN_PORT=80

# Run Flask app
CMD ["flask", "run"]
