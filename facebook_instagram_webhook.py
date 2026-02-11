"""
Facebook Messenger & Instagram Webhook Handler for Rasa
Handles incoming messages from Facebook Messenger and Instagram DMs
"""

import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)
warnings.filterwarnings("ignore", category=PendingDeprecationWarning)

import os
import logging
import requests
from flask import Flask, request, jsonify
import hashlib
import hmac

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Configuration from environment variables
VERIFY_TOKEN = os.getenv("FB_VERIFY_TOKEN")
PAGE_ACCESS_TOKEN = os.getenv("FB_PAGE_ACCESS_TOKEN")
APP_SECRET = os.getenv("FB_APP_SECRET")
RASA_URL = os.getenv("RASA_URL", "http://rasa:3000/webhooks/rest/webhook")

# Validate configuration
if not VERIFY_TOKEN:
    logger.error("FB_VERIFY_TOKEN not set!")
if not PAGE_ACCESS_TOKEN:
    logger.error("FB_PAGE_ACCESS_TOKEN not set!")
if not APP_SECRET:
    logger.warning("FB_APP_SECRET not set - signature verification disabled")


def verify_webhook_signature(payload, signature):
    """Verify that the webhook request came from Facebook"""
    if not APP_SECRET:
        return True  # Skip verification if secret not configured
    
    expected_signature = hmac.new(
        APP_SECRET.encode('utf-8'),
        payload,
        hashlib.sha256
    ).hexdigest()
    
    return hmac.compare_digest(f"sha256={expected_signature}", signature)


def send_facebook_message(recipient_id, message_text, platform="facebook"):
    """Send a message back to Facebook Messenger or Instagram"""
    try:
        if platform == "instagram":
            url = f"https://graph.facebook.com/v18.0/me/messages"
        else:
            url = f"https://graph.facebook.com/v18.0/me/messages"
        
        payload = {
            "recipient": {"id": recipient_id},
            "message": {"text": message_text}
        }
        
        headers = {
            "Content-Type": "application/json"
        }
        
        params = {
            "access_token": PAGE_ACCESS_TOKEN
        }
        
        response = requests.post(url, json=payload, params=params, headers=headers)
        response.raise_for_status()
        
        logger.info(f"Message sent successfully to {recipient_id} on {platform}")
        return True
        
    except Exception as e:
        logger.error(f"Error sending message to {platform}: {e}")
        return False


def send_facebook_buttons(recipient_id, text, buttons, platform="facebook"):
    """Send a message with buttons to Facebook Messenger or Instagram"""
    try:
        url = f"https://graph.facebook.com/v18.0/me/messages"
        
        # Convert Rasa buttons to Facebook button format
        fb_buttons = []
        for button in buttons[:3]:  # Facebook allows max 3 buttons
            payload = button.get("payload", "")
            if payload.startswith("http"):
                fb_buttons.append({
                    "type": "web_url",
                    "url": payload,
                    "title": button["title"]
                })
            else:
                fb_buttons.append({
                    "type": "postback",
                    "title": button["title"],
                    "payload": payload
                })
        
        message_payload = {
            "recipient": {"id": recipient_id},
            "message": {
                "attachment": {
                    "type": "template",
                    "payload": {
                        "template_type": "button",
                        "text": text,
                        "buttons": fb_buttons
                    }
                }
            }
        }
        
        params = {"access_token": PAGE_ACCESS_TOKEN}
        response = requests.post(url, json=message_payload, params=params)
        response.raise_for_status()
        
        logger.info(f"Button message sent to {recipient_id} on {platform}")
        return True
        
    except Exception as e:
        logger.error(f"Error sending buttons to {platform}: {e}")
        return False


def forward_to_rasa(sender_id, message_text, platform="facebook"):
    """Forward message to Rasa and send responses back"""
    try:
        logger.info(f"Forwarding to Rasa from {sender_id} ({platform}): {message_text}")
        
        payload = {
            "sender": f"{platform}_{sender_id}",  # Prefix with platform
            "message": message_text,
            "metadata": {
                "platform": platform,
                "source": platform
            }
        }
        
        response = requests.post(RASA_URL, json=payload, timeout=10)
        response.raise_for_status()
        
        rasa_responses = response.json()
        logger.info(f"Received {len(rasa_responses)} responses from Rasa")
        
        # Send each response back to user
        for rasa_msg in rasa_responses:
            if "text" in rasa_msg:
                if "buttons" in rasa_msg:
                    send_facebook_buttons(sender_id, rasa_msg["text"], rasa_msg["buttons"], platform)
                else:
                    send_facebook_message(sender_id, rasa_msg["text"], platform)
            elif "image" in rasa_msg:
                # TODO: Implement image sending
                logger.info(f"Image response not yet implemented: {rasa_msg['image']}")
        
        return True
        
    except Exception as e:
        logger.error(f"Error forwarding to Rasa: {e}")
        send_facebook_message(sender_id, "⚠️ Sorry, I'm having trouble processing your message right now.", platform)
        return False


@app.route('/webhooks/facebook/webhook', methods=['GET', 'POST'])
def facebook_webhook():
    """Handle Facebook Messenger and Instagram webhook requests"""
    
    if request.method == 'GET':
        # Webhook verification
        mode = request.args.get('hub.mode')
        token = request.args.get('hub.verify_token')
        challenge = request.args.get('hub.challenge')
        
        if mode == 'subscribe' and token == VERIFY_TOKEN:
            logger.info("Webhook verified successfully!")
            return challenge, 200
        else:
            logger.warning("Webhook verification failed!")
            return 'Verification failed', 403
    
    elif request.method == 'POST':
        # Verify signature
        signature = request.headers.get('X-Hub-Signature-256', '')
        if not verify_webhook_signature(request.data, signature):
            logger.warning("Invalid webhook signature!")
            return 'Invalid signature', 403
        
        # Process webhook data
        data = request.json
        
        if data.get('object') == 'page':
            for entry in data.get('entry', []):
                # Handle messaging events (Messenger & Instagram)
                for messaging_event in entry.get('messaging', []):
                    sender_id = messaging_event['sender']['id']
                    recipient_id = messaging_event['recipient']['id']
                    
                    # Determine platform (Instagram or Facebook)
                    platform = "instagram" if "instagram" in str(entry) else "facebook"
                    
                    # Handle message
                    if 'message' in messaging_event:
                        message = messaging_event['message']
                        
                        # Handle text message
                        if 'text' in message:
                            text = message['text']
                            forward_to_rasa(sender_id, text, platform)
                        
                        # Handle attachments (images, etc.)
                        elif 'attachments' in message:
                            # For now, send a generic response
                            send_facebook_message(sender_id, "I received your attachment, but I can only process text messages for now.", platform)
                    
                    # Handle postback (button clicks)
                    elif 'postback' in messaging_event:
                        payload = messaging_event['postback']['payload']
                        forward_to_rasa(sender_id, payload, platform)
        
        return 'OK', 200


@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "service": "facebook_instagram_webhook",
        "rasa_url": RASA_URL
    }), 200


if __name__ == '__main__':
    logger.info("Starting Facebook/Instagram Webhook Server...")
    logger.info(f"Rasa URL: {RASA_URL}")
    logger.info(f"Verify Token configured: {bool(VERIFY_TOKEN)}")
    logger.info(f"Page Access Token configured: {bool(PAGE_ACCESS_TOKEN)}")
    
    # Run Flask app
    app.run(host='0.0.0.0', port=5000, debug=False)
