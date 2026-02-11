import telebot
import requests
import os
import logging
import time

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Configuration from environment variables
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
# Note: Use the service name 'rasa' defined in docker-compose.yml
RASA_URL = os.getenv("RASA_URL", "http://rasa:3000/webhooks/rest/webhook")

if not TELEGRAM_TOKEN:
    logger.error("TELEGRAM_TOKEN environment variable not set. Please add it to Dokploy environment variables.")
    # Fallback for testing if token was provided in chat
    TELEGRAM_TOKEN = "8430682016:AAFIyYEH-JpNxP3zzXrGNX7wSYmy3mFWCUQ"
    logger.info("Using fallback token from code.")

bot = telebot.TeleBot(TELEGRAM_TOKEN)

def test_rasa_connection():
    logger.info(f"Testing connection to Rasa at {RASA_URL}...")
    try:
        # Check if Rasa is up (health check)
        health_url = RASA_URL.replace("/webhooks/rest/webhook", "/status")
        response = requests.get(health_url, timeout=5)
        if response.status_code == 200:
            logger.info("Successfully connected to Rasa server!")
            return True
        else:
            logger.warning(f"Rasa server returned status code {response.status_code}")
    except Exception as e:
        logger.error(f"Could not connect to Rasa server: {e}")
    return False

@bot.message_handler(func=lambda message: True)
def handle_all_messages(message):
    try:
        user_id = message.from_user.id
        text = message.text
        logger.info(f"Received message from user {user_id}: {text}")

        # Forward the message to Rasa
        payload = {
            "sender": str(user_id),
            "message": text
        }
        
        logger.info(f"Forwarding to Rasa: {payload}")
        response = requests.post(RASA_URL, json=payload, timeout=10)
        response.raise_for_status()
        
        rasa_responses = response.json()
        logger.info(f"Rasa responded: {rasa_responses}")

        # Send Rasa's responses back to the user
        if not rasa_responses:
            logger.warning("Rasa returned an empty response.")
            # Optional: bot.send_message(user_id, "I'm sorry, I'm having trouble processing that right now.")

        for rasa_msg in rasa_responses:
            if "text" in rasa_msg:
                bot.send_message(user_id, rasa_msg["text"])
            if "image" in rasa_msg:
                bot.send_photo(user_id, rasa_msg["image"])
            if "buttons" in rasa_msg:
                markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
                for button in rasa_msg["buttons"]:
                    markup.add(telebot.types.KeyboardButton(button["title"]))
                bot.send_message(user_id, "Choose an option:", reply_markup=markup)

    except Exception as e:
        logger.error(f"Error handling message: {e}")

if __name__ == "__main__":
    logger.info("Starting Telegram Polling Bridge...")
    
    # Wait for Rasa to be ready
    retries = 0
    while not test_rasa_connection() and retries < 10:
        retries += 1
        logger.info(f"Waiting for Rasa server... (Attempt {retries}/10)")
        time.sleep(10)

    logger.info("Polling for Telegram updates...")
    while True:
        try:
            bot.polling(none_stop=True, interval=0, timeout=20)
        except Exception as e:
            logger.error(f"Telegram polling crashed: {e}")
            time.sleep(5)
