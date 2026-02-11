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

# Default command to run Rasa server
CMD ["run", "--enable-api", "--cors", "*", "--debug"]
