# Dockerfile
FROM rasa/rasa:3.6.0-full

USER root

ENV PYTHONWARNINGS="ignore"

# Create directory for models and config
RUN mkdir -p /app/models /app/.config/rasa && chmod -R 777 /app/models /app/.config

# Copy project files
COPY . /app

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

USER 1001

# Start Rasa server
CMD ["run", "--enable-api", "--cors", "*", "--debug", "-p", "3000"]
