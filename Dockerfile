# Dockerfile
FROM rasa/rasa:3.6.0-full

USER root

# Create directory for models
RUN mkdir -p /app/models && chmod -R 777 /app/models

# Copy project files
COPY . /app

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

USER 1001

# Override entrypoint to allow running multiple processes
ENTRYPOINT []

# Start both Rasa server and Telegram Polling Bridge
CMD sh -c "rasa run --enable-api --cors '*' --debug -p 3000 & /opt/venv/bin/python telegram_poller.py"
