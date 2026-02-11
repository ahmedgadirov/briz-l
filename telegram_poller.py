import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)
warnings.filterwarnings("ignore", category=PendingDeprecationWarning)

import telebot
import requests
import os
import logging
import time
from collections import defaultdict

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Configuration from environment variables
TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")  # Match the .env variable name
# Note: Use 'localhost' since all services run in one container
RASA_URL = os.getenv("RASA_URL", "http://localhost:3000/webhooks/rest/webhook")

if not TELEGRAM_TOKEN:
    # Use the token provided in the chat as a fallback
    TELEGRAM_TOKEN = "8430682016:AAFIyYEH-JpNxP3zzXrGNX7wSYmy3mFWCUQ"
    logger.info("Using hardcoded fallback token.")

bot = telebot.TeleBot(TELEGRAM_TOKEN)

# Track processed updates and messages to prevent duplicates
processed_updates = set()
last_messages = defaultdict(lambda: {"text": None, "time": 0})
DUPLICATE_WINDOW = 5  # seconds

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

def is_duplicate_message(user_id, message_text, current_time):
    """Check if this message is a duplicate within the time window"""
    last = last_messages[user_id]
    
    if (last["text"] == message_text and 
        current_time - last["time"] < DUPLICATE_WINDOW):
        logger.warning(f"Duplicate message detected from {user_id}: {message_text}")
        return True
    
    # Update last message tracking
    last_messages[user_id] = {"text": message_text, "time": current_time}
    return False

def forward_to_rasa(user_id, message_text, is_button_click=False):
    try:
        # Send metadata to help Rasa understand the context
        metadata = {
            "is_button_click": is_button_click,
            "source": "telegram"
        }
        
        payload = {
            "sender": str(user_id),
            "message": message_text,
            "metadata": metadata
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
    # Check for duplicate messages
    current_time = time.time()
    if is_duplicate_message(message.from_user.id, message.text, current_time):
        logger.info(f"Skipping duplicate message from {message.from_user.id}")
        return
    
    logger.info(f"Incoming message from {message.from_user.id}: {message.text}")
    forward_to_rasa(message.from_user.id, message.text, is_button_click=False)

@bot.callback_query_handler(func=lambda call: True)
def handle_callback_query(call):
    # Check for duplicate callbacks using update_id if available
    if hasattr(call, 'id') and call.id in processed_updates:
        logger.info(f"Skipping duplicate callback: {call.id}")
        bot.answer_callback_query(call.id)
        return
    
    if hasattr(call, 'id'):
        processed_updates.add(call.id)
        # Keep only last 1000 update IDs to prevent memory bloat
        if len(processed_updates) > 1000:
            processed_updates.pop()
    
    logger.info(f"Incoming callback from {call.from_user.id}: {call.data}")
    # Forward the callback data (payload) to Rasa as a button click
    forward_to_rasa(call.from_user.id, call.data, is_button_click=True)
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
            # Polling without threaded parameter (removed in newer pyTelegramBotAPI versions)
            bot.polling(none_stop=True, interval=0, timeout=20)
        except Exception as e:
            logger.error(f"Telegram polling crashed: {e}")
            time.sleep(5)
