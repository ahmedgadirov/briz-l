# Dockerfile
FROM rasa/rasa:3.6.0-full

USER root

# Create directory for models
RUN mkdir -p /app/models && chmod -R 777 /app/models

# Copy project files
COPY . /app

USER 1001
