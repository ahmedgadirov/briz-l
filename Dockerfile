# Dockerfile
FROM rasa/rasa:3.6.0-full

USER root

ENV PYTHONWARNINGS="ignore::DeprecationWarning,ignore::PendingDeprecationWarning,ignore::ImportWarning"

# Create directory for models and config
RUN mkdir -p /app/models /app/.config/rasa && chmod -R 777 /app/models /app/.config

# Copy project files
COPY . /app

# Install dependencies (includes rasa-sdk for action server)
RUN pip install --no-cache-dir -r requirements.txt

# Make startup script executable
RUN chmod +x /app/start.sh

USER 1001

# Start all services using the startup script
CMD ["/bin/bash", "/app/start.sh"]
