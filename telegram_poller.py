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
RASA_URL = os.getenv("RASA_URL", "http://rasa:3000/webhooks/rest/webhook")

if not TELEGRAM_TOKEN:
    logger.error("TELEGRAM_TOKEN environment variable not set. Exiting.")
    exit(1)

bot = telebot.TeleBot(TELEGRAM_TOKEN)

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
        
        response = requests.post(RASA_URL, json=payload)
        response.raise_for_status()
        
        rasa_responses = response.json()
        logger.info(f"Rasa responded: {rasa_responses}")

        # Send Rasa's responses back to the user
        for rasa_msg in rasa_responses:
            if "text" in rasa_msg:
                bot.send_message(user_id, rasa_msg["text"])
            if "image" in rasa_msg:
                bot.send_photo(user_id, rasa_msg["image"])
            if "buttons" in rasa_msg:
                markup = telebot.types.InlineKeyboardMarkup()
                for button in rasa_msg["buttons"]:
                    markup.add(telebot.types.InlineKeyboardButton(text=button["title"], callback_data=button["payload"]))
                bot.send_message(user_id, "Choose an option:", reply_markup=markup)

    except Exception as e:
        logger.error(f"Error handling message: {e}")

@bot.callback_query_handler(func=lambda call: True)
def handle_callback_query(call):
    try:
        user_id = call.from_user.id
        payload = call.data
        logger.info(f"Received callback query from user {user_id}: {payload}")

        # Forward the button click to Rasa
        rasa_payload = {
            "sender": str(user_id),
            "message": payload
        }
        
        response = requests.post(RASA_URL, json=rasa_payload)
        response.raise_for_status()
        
        rasa_responses = response.json()

        for rasa_msg in rasa_responses:
            if "text" in rasa_msg:
                bot.send_message(user_id, rasa_msg["text"])

    except Exception as e:
        logger.error(f"Error handling callback query: {e}")

if __name__ == "__main__":
    logger.info("Starting Telegram Polling Bridge...")
    while True:
        try:
            bot.polling(none_stop=True, interval=0, timeout=20)
        except Exception as e:
            logger.error(f"Telegram polling crashed: {e}")
            time.sleep(5)
