# Dockerfile
FROM rasa/rasa:3.6.0-full

USER root

ENV PYTHONWARNINGS="ignore"

# Create directory for models
RUN mkdir -p /app/models && chmod -R 777 /app/models

# Copy project files
COPY . /app

# Install dependencies
RUN pip install --upgrade pip setuptools wheel
RUN pip install --no-cache-dir -r requirements.txt

USER 1001

# Start Rasa server
CMD ["run", "--enable-api", "--cors", "*", "--debug", "-p", "3000"]
