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
import json

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Load environment variables from .env file
load_dotenv()

# Import admin handler for Seljan
try:
    from admin_handler import is_admin, generate_admin_greeting
    ADMIN_HANDLER_AVAILABLE = True
except ImportError:
    ADMIN_HANDLER_AVAILABLE = False
    logger.warning("Admin handler not available")

app = Flask(__name__)

# Configuration from environment variables
FB_VERIFY_TOKEN = os.getenv("FB_VERIFY_TOKEN")
FB_PAGE_ACCESS_TOKEN = os.getenv("FB_PAGE_ACCESS_TOKEN")
FB_APP_SECRET = os.getenv("FB_APP_SECRET")
FB_PAGE_ID = os.getenv("FB_PAGE_ID")
INSTAGRAM_ACCOUNT_ID = os.getenv("INSTAGRAM_ACCOUNT_ID")

WA_VERIFY_TOKEN = os.getenv("WA_VERIFY_TOKEN")
WA_ACCESS_TOKEN = os.getenv("WA_ACCESS_TOKEN")
WA_PHONE_NUMBER_ID = os.getenv("WA_PHONE_NUMBER_ID")

RASA_URL = os.getenv("RASA_URL", "http://rasa:3000/webhooks/rest/webhook")
SKIP_VERIFY_SIGNATURE = os.getenv("SKIP_VERIFY_SIGNATURE", "false").lower() == "true"

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
        
    if not signature:
        logger.warning("Missing X-Hub-Signature-256 header")
        return False
    
    expected_signature = hmac.new(
        secret.encode('utf-8'),
        payload,
        hashlib.sha256
    ).hexdigest()
    
    # Prefix required by Facebook
    expected_full = f"sha256={expected_signature}"
    
    is_valid = hmac.compare_digest(expected_full, signature)
    
    if not is_valid:
        if not SKIP_VERIFY_SIGNATURE:
            logger.warning(f"Signature mismatch!")
            logger.warning(f"  Received: {signature[:15]}...")
            logger.warning(f"  Expected prefix: {expected_full[:15]}...")
            logger.warning(f"  Secret starts with: {secret[:4]}...")
            logger.warning(f"  Payload size: {len(payload)} bytes")
            if payload:
                logger.info(f"  Payload preview: {payload[:100]}...")
            
    return is_valid or SKIP_VERIFY_SIGNATURE


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

def send_facebook_message(recipient_id, message_text, platform="facebook"):
    """Send a message back to Facebook Messenger or Instagram"""
    try:
        # Determine the correct node (Account ID or 'me')
        node = "me"
        if platform == "instagram" and INSTAGRAM_ACCOUNT_ID:
            node = INSTAGRAM_ACCOUNT_ID
            logger.info(f"Using Instagram Account ID: {node}")
        elif platform == "facebook" and FB_PAGE_ID:
            node = FB_PAGE_ID
            logger.info(f"Using Facebook Page ID: {node}")
            
        url = f"https://graph.facebook.com/v18.0/{node}/messages"
        
        payload = {
            "messaging_type": "RESPONSE",
            "recipient": {"id": recipient_id},
            "message": {"text": message_text}
        }
        
        params = {"access_token": FB_PAGE_ACCESS_TOKEN}
        
        response = requests.post(url, json=payload, params=params)
        
        if not response.ok:
            logger.error(f"Graph send failed {response.status_code}: {response.text}")
            
        response.raise_for_status()
        
        logger.info(f"Message sent successfully to {recipient_id} ({platform})")
        return True
        
    except Exception as e:
        logger.error(f"Error sending {platform} message: {e}")
        return False


def send_facebook_buttons(recipient_id, text, buttons, platform="facebook"):
    """Send a message with buttons to Facebook Messenger or Instagram"""
    try:
        # Determine the correct node (Account ID or 'me')
        node = "me"
        if platform == "instagram" and INSTAGRAM_ACCOUNT_ID:
            node = INSTAGRAM_ACCOUNT_ID
            logger.info(f"Using Instagram Account ID: {node}")
        elif platform == "facebook" and FB_PAGE_ID:
            node = FB_PAGE_ID
            logger.info(f"Using Facebook Page ID: {node}")
            
        url = f"https://graph.facebook.com/v18.0/{node}/messages"
        
        # Convert Rasa buttons to Facebook button format
        fb_buttons = []
        for button in buttons[:3]:  # Facebook allows max 3 buttons
            button_payload = button.get("payload", "")
            if button_payload.startswith("http"):
                fb_buttons.append({
                    "type": "web_url",
                    "url": button_payload,
                    "title": button["title"]
                })
            else:
                fb_buttons.append({
                    "type": "postback",
                    "title": button["title"],
                    "payload": button_payload[:64]  # Limit
                })
        
        message_payload = {
            "messaging_type": "RESPONSE",
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
        
        if not response.ok:
            logger.error(f"Graph buttons send failed {response.status_code}: {response.text}")
            
        response.raise_for_status()
        
        logger.info(f"Button message sent to {recipient_id} ({platform})")
        return True
        
    except Exception as e:
        logger.error(f"Error sending buttons to {platform}: {e}")
        return False


def handle_facebook_responses(recipient_id, rasa_responses, platform="facebook"):
    """Send Rasa responses back to Facebook/Instagram"""
    for rasa_msg in rasa_responses:
        if "text" in rasa_msg:
            if "buttons" in rasa_msg and platform != "instagram":
                # Only use button templates for Facebook (Messenger)
                send_facebook_buttons(recipient_id, rasa_msg["text"], rasa_msg["buttons"], platform)
            else:
                # For instagram: turn buttons into a numbered text list (button templates often fail)
                if "buttons" in rasa_msg and platform == "instagram":
                    btns = rasa_msg["buttons"][:3]
                    opts = "\n".join([f"{i+1}) {b['title']}" for i, b in enumerate(btns)])
                    text = f"{rasa_msg['text']}\n\n{opts}"
                    send_facebook_message(recipient_id, text, platform)
                else:
                    send_facebook_message(recipient_id, rasa_msg["text"], platform)
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
        try:
            # Capture raw data early
            raw_data = request.get_data(cache=True)
            signature = request.headers.get('X-Hub-Signature-256', '')
            
            # Verify signature BEFORE parsing JSON
            if FB_APP_SECRET and not verify_webhook_signature(raw_data, signature, FB_APP_SECRET):
                logger.warning("Invalid Facebook webhook signature!")
                return 'Invalid signature', 403
                
            # Process webhook data - Use json.loads for robustness against Content-Type issues
            try:
                data = json.loads(raw_data.decode('utf-8'))
            except Exception as e:
                logger.error(f"FB webhook 400: invalid JSON. content_type={request.content_type} raw={raw_data[:500]!r}")
                logger.error(f"Headers: {dict(request.headers)}")
                return 'Invalid JSON', 400
            
            obj = data.get('object')
            if obj not in ('page', 'instagram'):
                logger.warning(f"FB webhook: unknown object type '{obj}'. Ignoring.")
                return 'OK', 200
            
            for entry in data.get('entry', []):
                # Instagram and Page events usually use 'messaging'
                for messaging_event in entry.get('messaging', []):
                    sender_id = messaging_event['sender']['id']
                    
                    # Determine platform
                    platform = "instagram" if obj == "instagram" else "facebook"
                    
                    # Handle message
                    if 'message' in messaging_event:
                        message = messaging_event['message']
                        if 'text' in message:
                            text = message['text']
                            rasa_responses = forward_to_rasa(sender_id, text, platform)
                            handle_facebook_responses(sender_id, rasa_responses, platform)
                        elif 'attachments' in message:
                            send_facebook_message(sender_id, "I can only process text messages for now.", platform)
                    
                    # Handle postback (button clicks)
                    elif 'postback' in messaging_event:
                        payload = messaging_event['postback']['payload']
                        rasa_responses = forward_to_rasa(sender_id, payload, platform)
                        handle_facebook_responses(sender_id, rasa_responses, platform)
                        
            return 'OK', 200
            
        except Exception as e:
            logger.exception(f"FB webhook error: {e}")
            return 'Error', 500


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
        try:
            # Capture raw data early
            raw_data = request.get_data(cache=True)
            signature = request.headers.get('X-Hub-Signature-256', '')
            
            # Verify signature (optional) BEFORE parsing JSON
            if FB_APP_SECRET and not verify_webhook_signature(raw_data, signature, FB_APP_SECRET):
                logger.warning("Invalid WhatsApp webhook signature!")
                return 'Invalid signature', 403
                
            # Process webhook data - Use json.loads for robustness against Content-Type issues
            try:
                data = json.loads(raw_data.decode('utf-8'))
            except Exception as e:
                logger.error(f"WA webhook 400: invalid JSON. content_type={request.content_type} raw={raw_data[:500]!r}")
                logger.error(f"Headers: {dict(request.headers)}")
                return 'Invalid JSON', 400
            
            if data.get('object') != 'whatsapp_business_account':
                logger.warning(f"WA webhook: unknown object type '{data.get('object')}'. Ignoring.")
                return 'OK', 200
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
            
        except Exception as e:
            logger.exception(f"WA webhook error: {e}")
            return 'Error', 500


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
        "instagram_configured": bool(INSTAGRAM_ACCOUNT_ID),
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
    logger.info(f"  - Page Access Token: {bool(FB_PAGE_ACCESS_TOKEN)} (starts with: {FB_PAGE_ACCESS_TOKEN[:4] if FB_PAGE_ACCESS_TOKEN else 'None'}...)")
    logger.info(f"  - Page ID: {bool(FB_PAGE_ID)} ({FB_PAGE_ID if FB_PAGE_ID else 'Not set'})")
    logger.info(f"  - Instagram Account ID: {bool(INSTAGRAM_ACCOUNT_ID)} ({INSTAGRAM_ACCOUNT_ID if INSTAGRAM_ACCOUNT_ID else 'Not set'})")
    logger.info(f"  - App Secret: {bool(FB_APP_SECRET)} (starts with: {FB_APP_SECRET[:4] if FB_APP_SECRET else 'None'}...)")
    logger.info(f"  - Skip Signature Verify: {SKIP_VERIFY_SIGNATURE}")
    logger.info(f"WhatsApp:")
    wa_token_prefix = WA_VERIFY_TOKEN[0] if WA_VERIFY_TOKEN else "None"
    logger.info(f"  - Verify Token: {bool(WA_VERIFY_TOKEN)} (starts with: {wa_token_prefix}...)")
    logger.info(f"  - Access Token: {bool(WA_ACCESS_TOKEN)}")
    logger.info(f"  - Phone Number ID: {bool(WA_PHONE_NUMBER_ID)}")
    logger.info("=" * 60)
    
    # Run Flask app
    port = int(os.getenv("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=False)