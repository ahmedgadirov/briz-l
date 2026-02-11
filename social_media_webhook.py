"""
Unified Social Media Webhook Handler for Rasa
Handles Facebook Messenger, Instagram DMs, and WhatsApp in one service
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
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Import admin handler for Seljan
try:
    from admin_handler import is_admin, generate_admin_greeting
    ADMIN_HANDLER_AVAILABLE = True
except ImportError:
    ADMIN_HANDLER_AVAILABLE = False
    logger.warning("Admin handler not available")

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Configuration from environment variables
FB_VERIFY_TOKEN = os.getenv("FB_VERIFY_TOKEN")
FB_PAGE_ACCESS_TOKEN = os.getenv("FB_PAGE_ACCESS_TOKEN")
FB_APP_SECRET = os.getenv("FB_APP_SECRET")

WA_VERIFY_TOKEN = os.getenv("WA_VERIFY_TOKEN")
WA_ACCESS_TOKEN = os.getenv("WA_ACCESS_TOKEN")
WA_PHONE_NUMBER_ID = os.getenv("WA_PHONE_NUMBER_ID")

RASA_URL = os.getenv("RASA_URL", "http://rasa:3000/webhooks/rest/webhook")

# Validate configuration
if not FB_VERIFY_TOKEN:
    logger.error("FB_VERIFY_TOKEN not set!")
if not FB_PAGE_ACCESS_TOKEN:
    logger.warning("FB_PAGE_ACCESS_TOKEN not set!")
if not WA_VERIFY_TOKEN:
    logger.error("WA_VERIFY_TOKEN not set!")
if not WA_ACCESS_TOKEN:
    logger.warning("WA_ACCESS_TOKEN not set!")


# ============================================================================
# COMMON FUNCTIONS
# ============================================================================

def normalize_phone(phone):
    """Normalize phone number to E.164-like format (digits only)"""
    if not phone:
        return ""
    # Remove +, spaces, dashes, and parentheses
    clean_phone = "".join(filter(str.isdigit, str(phone)))
    
    # If it starts with 0 (local Azerbaijan format), replace with 994
    if clean_phone.startswith("0") and len(clean_phone) == 10:
        clean_phone = "994" + clean_phone[1:]
    
    return clean_phone


def verify_webhook_signature(payload, signature, secret):
    """Verify that the webhook request came from Facebook/WhatsApp"""
    if not secret:
        return True  # Skip verification if secret not configured
    
    expected_signature = hmac.new(
        secret.encode('utf-8'),
        payload,
        hashlib.sha256
    ).hexdigest()
    
    # Prefix required by Facebook
    expected_full = f"sha256={expected_signature}"
    
    is_valid = hmac.compare_digest(expected_full, signature)
    
    if not is_valid:
        logger.warning(f"Signature mismatch!")
        logger.warning(f"  Received: {signature[:15]}...")
        logger.warning(f"  Expected prefix: {expected_full[:15]}...")
        logger.debug(f"  Payload size: {len(payload)} bytes")
        
    return is_valid


def forward_to_rasa(sender_id, message_text, platform="unknown"):
    """Forward message to Rasa and return responses"""
    try:
        logger.info(f"Forwarding to Rasa from {sender_id} ({platform}): {message_text}")
        
        payload = {
            "sender": f"{platform}_{sender_id}",
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
        return rasa_responses
        
    except Exception as e:
        logger.error(f"Error forwarding to Rasa: {e}")
        return []


# ============================================================================
# FACEBOOK & INSTAGRAM FUNCTIONS
# ============================================================================

def send_facebook_message(recipient_id, message_text):
    """Send a message back to Facebook Messenger or Instagram"""
    try:
        url = f"https://graph.facebook.com/v18.0/me/messages"
        
        payload = {
            "recipient": {"id": recipient_id},
            "message": {"text": message_text}
        }
        
        params = {"access_token": FB_PAGE_ACCESS_TOKEN}
        
        response = requests.post(url, json=payload, params=params)
        response.raise_for_status()
        
        logger.info(f"Message sent successfully to {recipient_id}")
        return True
        
    except Exception as e:
        logger.error(f"Error sending Facebook message: {e}")
        return False


def send_facebook_buttons(recipient_id, text, buttons):
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
                    "payload": payload[:64]  # Telegram limit
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
        
        params = {"access_token": FB_PAGE_ACCESS_TOKEN}
        response = requests.post(url, json=message_payload, params=params)
        response.raise_for_status()
        
        logger.info(f"Button message sent to {recipient_id}")
        return True
        
    except Exception as e:
        logger.error(f"Error sending buttons: {e}")
        return False


def handle_facebook_responses(recipient_id, rasa_responses):
    """Send Rasa responses back to Facebook/Instagram"""
    for rasa_msg in rasa_responses:
        if "text" in rasa_msg:
            if "buttons" in rasa_msg:
                send_facebook_buttons(recipient_id, rasa_msg["text"], rasa_msg["buttons"])
            else:
                send_facebook_message(recipient_id, rasa_msg["text"])
        elif "image" in rasa_msg:
            logger.info(f"Image response not yet implemented: {rasa_msg['image']}")


# ============================================================================
# WHATSAPP FUNCTIONS
# ============================================================================

def send_whatsapp_message(recipient_phone, message_text):
    """Send a text message via WhatsApp Business API"""
    try:
        if not WA_PHONE_NUMBER_ID or not WA_ACCESS_TOKEN:
            logger.error("WhatsApp credentials not configured!")
            return False
        
        # Normalize phone number
        normalized_phone = normalize_phone(recipient_phone)
        logger.info(f"Sending WhatsApp to {normalized_phone} (original: {recipient_phone})")

        url = f"https://graph.facebook.com/v18.0/{WA_PHONE_NUMBER_ID}/messages"
        
        headers = {
            "Authorization": f"Bearer {WA_ACCESS_TOKEN}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": normalized_phone,
            "type": "text",
            "text": {
                "preview_url": False,
                "body": message_text
            }
        }
        
        response = requests.post(url, json=payload, headers=headers, timeout=10)
        
        if response.status_code != 200:
            logger.error(f"WhatsApp API Error (Status {response.status_code}): {response.text}")
            
        response.raise_for_status()
        
        logger.info(f"WhatsApp message sent successfully to {normalized_phone}")
        return True
        
    except Exception as e:
        logger.error(f"Error sending WhatsApp message: {e}")
        return False


def send_whatsapp_template(recipient_phone, template_name, language_code="en", parameters=None):
    """Send a WhatsApp template message"""
    try:
        if not WA_PHONE_NUMBER_ID or not WA_ACCESS_TOKEN:
            logger.error("WhatsApp credentials not configured!")
            return False
        
        # Normalize phone number
        normalized_phone = normalize_phone(recipient_phone)
        logger.info(f"Sending WhatsApp Template '{template_name}' to {normalized_phone}")

        url = f"https://graph.facebook.com/v18.0/{WA_PHONE_NUMBER_ID}/messages"
        
        headers = {
            "Authorization": f"Bearer {WA_ACCESS_TOKEN}",
            "Content-Type": "application/json"
        }
        
        template_components = []
        if parameters:
            template_components.append({
                "type": "body",
                "parameters": [{"type": "text", "text": str(param)} for param in parameters]
            })
        
        payload = {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": normalized_phone,
            "type": "template",
            "template": {
                "name": template_name,
                "language": {"code": language_code},
                "components": template_components
            }
        }
        
        response = requests.post(url, json=payload, headers=headers, timeout=10)
        
        if response.status_code != 200:
            logger.error(f"WhatsApp Template API Error (Status {response.status_code}): {response.text}")

        response.raise_for_status()
        
        logger.info(f"WhatsApp template sent to {normalized_phone}")
        return True
        
    except Exception as e:
        logger.error(f"Error sending WhatsApp template: {e}")
        return False


def mark_whatsapp_read(message_id):
    """Mark a WhatsApp message as read"""
    try:
        url = f"https://graph.facebook.com/v18.0/{WA_PHONE_NUMBER_ID}/messages"
        
        headers = {
            "Authorization": f"Bearer {WA_ACCESS_TOKEN}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "messaging_product": "whatsapp",
            "status": "read",
            "message_id": message_id
        }
        
        response = requests.post(url, json=payload, headers=headers, timeout=5)
        response.raise_for_status()
        return True
        
    except Exception as e:
        logger.error(f"Error marking message as read: {e}")
        return False


def handle_whatsapp_responses(recipient_phone, rasa_responses):
    """Send Rasa responses back to WhatsApp"""
    for rasa_msg in rasa_responses:
        if "text" in rasa_msg:
            send_whatsapp_message(recipient_phone, rasa_msg["text"])
        elif "image" in rasa_msg:
            logger.info(f"Image response not yet implemented: {rasa_msg['image']}")


# ============================================================================
# WEBHOOK ENDPOINTS
# ============================================================================

@app.route('/webhooks/facebook/webhook', methods=['GET', 'POST'])
def facebook_webhook():
    """Handle Facebook Messenger and Instagram webhook requests"""
    
    if request.method == 'GET':
        # Webhook verification
        mode = request.args.get('hub.mode')
        token = request.args.get('hub.verify_token')
        challenge = request.args.get('hub.challenge')
        
        logger.info(f"Facebook verification attempt:")
        logger.info(f"  Mode: {mode}")
        logger.info(f"  Received token: {token}")
        logger.info(f"  Expected token: {FB_VERIFY_TOKEN}")
        logger.info(f"  Challenge: {challenge}")
        
        if mode == 'subscribe' and token and FB_VERIFY_TOKEN and token == FB_VERIFY_TOKEN:
            logger.info("✅ Facebook/Instagram webhook verified successfully!")
            return challenge, 200
        else:
            logger.warning(f"❌ Facebook/Instagram webhook verification failed!")
            logger.warning(f"   Reason: mode={mode}, token_matches={token == FB_VERIFY_TOKEN}")
            return 'Verification failed', 403
    
    elif request.method == 'POST':
        # Verify signature
        signature = request.headers.get('X-Hub-Signature-256', '')
        if FB_APP_SECRET and not verify_webhook_signature(request.data, signature, FB_APP_SECRET):
            logger.warning("Invalid Facebook webhook signature!")
            return 'Invalid signature', 403
        
        # Process webhook data
        data = request.json
        
        if data.get('object') == 'page':
            for entry in data.get('entry', []):
                for messaging_event in entry.get('messaging', []):
                    sender_id = messaging_event['sender']['id']
                    
                    # Determine platform
                    platform = "instagram" if "instagram" in str(entry) else "facebook"
                    
                    # Handle message
                    if 'message' in messaging_event:
                        message = messaging_event['message']
                        
                        if 'text' in message:
                            text = message['text']
                            rasa_responses = forward_to_rasa(sender_id, text, platform)
                            handle_facebook_responses(sender_id, rasa_responses)
                        
                        elif 'attachments' in message:
                            send_facebook_message(sender_id, "I can only process text messages for now.")
                    
                    # Handle postback (button clicks)
                    elif 'postback' in messaging_event:
                        payload = messaging_event['postback']['payload']
                        rasa_responses = forward_to_rasa(sender_id, payload, platform)
                        handle_facebook_responses(sender_id, rasa_responses)
        
        return 'OK', 200


@app.route('/webhooks/whatsapp/webhook', methods=['GET', 'POST'])
def whatsapp_webhook():
    """Handle WhatsApp webhook requests"""
    
    if request.method == 'GET':
        # Webhook verification
        mode = request.args.get('hub.mode')
        token = request.args.get('hub.verify_token')
        challenge = request.args.get('hub.challenge')
        
        if mode == 'subscribe' and token == WA_VERIFY_TOKEN:
            logger.info("WhatsApp webhook verified successfully!")
            return challenge, 200
        else:
            logger.warning("WhatsApp webhook verification failed!")
            return 'Verification failed', 403
    
    elif request.method == 'POST':
        # Verify signature (optional)
        signature = request.headers.get('X-Hub-Signature-256', '')
        if FB_APP_SECRET and not verify_webhook_signature(request.data, signature, FB_APP_SECRET):
            logger.warning("Invalid WhatsApp webhook signature!")
            return 'Invalid signature', 403
        
        # Process webhook data
        data = request.json
        
        if data.get('object') == 'whatsapp_business_account':
            for entry in data.get('entry', []):
                for change in entry.get('changes', []):
                    value = change.get('value', {})
                    
                    if 'messages' in value:
                        for message in value['messages']:
                            message_id = message.get('id')
                            from_phone = message.get('from')
                            message_type = message.get('type')
                            
                            # Mark as read
                            if message_id:
                                mark_whatsapp_read(message_id)
                            
                            # Handle text messages
                            if message_type == 'text':
                                text = message.get('text', {}).get('body', '')
                                if text:
                                    rasa_responses = forward_to_rasa(from_phone, text, "whatsapp")
                                    handle_whatsapp_responses(from_phone, rasa_responses)
                            
                            # Handle button/interactive replies
                            elif message_type in ['button', 'interactive']:
                                reply_text = ""
                                if message_type == 'button':
                                    reply_text = message.get('button', {}).get('text', '')
                                elif message_type == 'interactive':
                                    interactive = message.get('interactive', {})
                                    if 'button_reply' in interactive:
                                        reply_text = interactive['button_reply'].get('title', '')
                                    elif 'list_reply' in interactive:
                                        reply_text = interactive['list_reply'].get('title', '')
                                
                                if reply_text:
                                    rasa_responses = forward_to_rasa(from_phone, reply_text, "whatsapp")
                                    handle_whatsapp_responses(from_phone, rasa_responses)
                            
                            else:
                                send_whatsapp_message(from_phone, "I can only process text messages at the moment.")
        
        return 'OK', 200


# ============================================================================
# API ENDPOINTS FOR SENDING MESSAGES
# ============================================================================

@app.route('/whatsapp/send', methods=['POST'])
def send_whatsapp_api():
    """API endpoint to send WhatsApp messages (for reports/notifications)"""
    try:
        data = request.json
        phone = data.get('phone')
        message = data.get('message')
        
        if not phone or not message:
            return jsonify({"error": "Missing phone or message"}), 400
        
        success = send_whatsapp_message(phone, message)
        
        if success:
            return jsonify({"status": "sent", "phone": phone}), 200
        else:
            return jsonify({"error": "Failed to send message"}), 500
            
    except Exception as e:
        logger.error(f"Error in send_whatsapp_api: {e}")
        return jsonify({"error": str(e)}), 500


@app.route('/whatsapp/send-template', methods=['POST'])
def send_whatsapp_template_api():
    """API endpoint to send WhatsApp template messages"""
    try:
        data = request.json
        phone = data.get('phone')
        template = data.get('template')
        language = data.get('language', 'en')
        parameters = data.get('parameters', [])
        
        if not phone or not template:
            return jsonify({"error": "Missing phone or template"}), 400
        
        success = send_whatsapp_template(phone, template, language, parameters)
        
        if success:
            return jsonify({"status": "sent", "phone": phone, "template": template}), 200
        else:
            return jsonify({"error": "Failed to send template"}), 500
            
    except Exception as e:
        logger.error(f"Error in send_whatsapp_template_api: {e}")
        return jsonify({"error": str(e)}), 500


@app.route('/health', methods=['GET'])
@app.route('/webhooks/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "service": "social_media_webhook",
        "rasa_url": RASA_URL,
        "facebook_configured": bool(FB_PAGE_ACCESS_TOKEN),
        "whatsapp_configured": bool(WA_ACCESS_TOKEN and WA_PHONE_NUMBER_ID)
    }), 200


# ============================================================================
# MAIN
# ============================================================================

if __name__ == '__main__':
    logger.info("=" * 60)
    logger.info("Starting Unified Social Media Webhook Server")
    logger.info("=" * 60)
    logger.info(f"Rasa URL: {RASA_URL}")
    logger.info(f"Facebook/Instagram:")
    # Log only first character of verify token for security
    fb_token_prefix = FB_VERIFY_TOKEN[0] if FB_VERIFY_TOKEN else "None"
    logger.info(f"  - Verify Token: {bool(FB_VERIFY_TOKEN)} (starts with: {fb_token_prefix}...)")
    logger.info(f"  - Page Access Token: {bool(FB_PAGE_ACCESS_TOKEN)}")
    logger.info(f"  - App Secret: {bool(FB_APP_SECRET)}")
    logger.info(f"WhatsApp:")
    wa_token_prefix = WA_VERIFY_TOKEN[0] if WA_VERIFY_TOKEN else "None"
    logger.info(f"  - Verify Token: {bool(WA_VERIFY_TOKEN)} (starts with: {wa_token_prefix}...)")
    logger.info(f"  - Access Token: {bool(WA_ACCESS_TOKEN)}")
    logger.info(f"  - Phone Number ID: {bool(WA_PHONE_NUMBER_ID)}")
    logger.info("=" * 60)
    
    # Run Flask app
    port = int(os.getenv("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
