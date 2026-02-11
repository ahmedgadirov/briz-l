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
# Note: Use localhost if running in the same container, or 'rasa' if in separate containers
RASA_URL = os.getenv("RASA_URL", "http://localhost:3000/webhooks/rest/webhook")

if not TELEGRAM_TOKEN:
    # Use the token provided in the chat as a fallback
    TELEGRAM_TOKEN = "8430682016:AAFIyYEH-JpNxP3zzXrGNX7wSYmy3mFWCUQ"
    logger.info("Using hardcoded fallback token.")

bot = telebot.TeleBot(TELEGRAM_TOKEN)

def test_rasa_connection():
    logger.info(f"Testing connection to Rasa at {RASA_URL}...")
    try:
        health_url = RASA_URL.replace("/webhooks/rest/webhook", "/status")
        response = requests.get(health_url, timeout=5)
        if response.status_code == 200:
            logger.info(f"Successfully connected to Rasa server! Status: {response.json()}")
            return True
        else:
            logger.warning(f"Rasa server returned status code {response.status_code}")
    except Exception as e:
        logger.error(f"Could not connect to Rasa server at {RASA_URL}: {e}")
    return False

def forward_to_rasa(user_id, message_text):
    try:
        payload = {
            "sender": str(user_id),
            "message": message_text
        }
        logger.debug(f"--- Sending to Rasa ---")
        logger.debug(f"Payload: {payload}")
        
        response = requests.post(RASA_URL, json=payload, timeout=10)
        response.raise_for_status()
        
        rasa_responses = response.json()
        logger.debug(f"--- Received from Rasa ---")
        logger.debug(f"Responses: {rasa_responses}")

        for rasa_msg in rasa_responses:
            if "text" in rasa_msg:
                # Handle simple text
                if "buttons" in rasa_msg:
                    markup = telebot.types.InlineKeyboardMarkup()
                    for button in rasa_msg["buttons"]:
                        payload = button.get("payload", "")
                        is_url = button.get("type") == "web_url" or payload.startswith("http")
                        
                        if is_url:
                            markup.add(telebot.types.InlineKeyboardButton(text=button["title"], url=payload))
                        else:
                            # Telegram callback_data has a 64 byte limit
                            callback_data = payload[:64]
                            markup.add(telebot.types.InlineKeyboardButton(text=button["title"], callback_data=callback_data))
                    bot.send_message(user_id, rasa_msg["text"], reply_markup=markup)
                else:
                    bot.send_message(user_id, rasa_msg["text"])
            
            elif "image" in rasa_msg:
                bot.send_photo(user_id, rasa_msg["image"])
            
            elif "buttons" in rasa_msg:
                # Case where buttons are sent without a separate 'text' field (rare but possible)
                markup = telebot.types.InlineKeyboardMarkup()
                for button in rasa_msg["buttons"]:
                    payload = button.get("payload", "")
                    is_url = button.get("type") == "web_url" or payload.startswith("http")
                    
                    if is_url:
                        markup.add(telebot.types.InlineKeyboardButton(text=button["title"], url=payload))
                    else:
                        callback_data = payload[:64]
                        markup.add(telebot.types.InlineKeyboardButton(text=button["title"], callback_data=callback_data))
                bot.send_message(user_id, "Choose an option:", reply_markup=markup)

    except Exception as e:
        logger.error(f"Error forwarding to Rasa: {e}")
        bot.send_message(user_id, "⚠️ Error: Could not connect to the bot engine.")

@bot.message_handler(func=lambda message: True)
def handle_all_messages(message):
    logger.info(f"Incoming message from {message.from_user.id}: {message.text}")
    forward_to_rasa(message.from_user.id, message.text)

@bot.callback_query_handler(func=lambda call: True)
def handle_callback_query(call):
    logger.info(f"Incoming callback from {call.from_user.id}: {call.data}")
    # Forward the callback data (payload) to Rasa
    forward_to_rasa(call.from_user.id, call.data)
    # Answer the callback to remove the loading state in Telegram
    bot.answer_callback_query(call.id)

if __name__ == "__main__":
    logger.info("Starting Telegram Polling Bridge...")
    
    # Wait for Rasa to be ready
    retries = 0
    while not test_rasa_connection() and retries < 15:
        retries += 1
        logger.info(f"Waiting for Rasa server... (Attempt {retries}/15)")
        time.sleep(10)

    logger.info("Polling for Telegram updates...")
    while True:
        try:
            bot.polling(none_stop=True, interval=0, timeout=20)
        except Exception as e:
            logger.error(f"Telegram polling crashed: {e}")
            time.sleep(5)
