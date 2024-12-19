# Use the official Python slim image as the base image
FROM python:3.9-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install Gunicorn explicitly
RUN pip install --no-cache-dir gunicorn

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire project directory into the container
COPY . .

# Expose the port that Django's development server will use
EXPOSE 8000

# Default environment variable for the action to perform
ENV ACTION=runserver

# Entry point to dynamically determine the command to run
ENTRYPOINT ["sh", "-c", "if [ \"$ACTION\" = \"runpipeline\" ]; then \
    python manage.py $ACTION; \
  else \
    gunicorn project.wsgi:application --bind 0.0.0.0:8000 --workers 3; \
  fi"]
