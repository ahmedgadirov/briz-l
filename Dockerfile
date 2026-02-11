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

# Expose ports for all services
EXPOSE 3000 5000 5055

USER 1001

# Override the entrypoint and start all services using the startup script
ENTRYPOINT []
CMD ["/bin/bash", "/app/start.sh"]
