"""
WhatsApp Business API Webhook Handler and Report Sender for Rasa
Handles incoming messages from WhatsApp and sends reports/notifications
"""

import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)
warnings.filterwarnings("ignore", category=PendingDeprecationWarning)

import os
import logging
import requests
from flask import Flask, request, jsonify
import hmac
import hashlib

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Configuration from environment variables
VERIFY_TOKEN = os.getenv("WA_VERIFY_TOKEN")
ACCESS_TOKEN = os.getenv("WA_ACCESS_TOKEN")
PHONE_NUMBER_ID = os.getenv("WA_PHONE_NUMBER_ID")
APP_SECRET = os.getenv("FB_APP_SECRET")  # Same as Facebook App Secret
RASA_URL = os.getenv("RASA_URL", "http://rasa:3000/webhooks/rest/webhook")

# WhatsApp API Base URL
WA_API_URL = f"https://graph.facebook.com/v18.0/{PHONE_NUMBER_ID}/messages"

# Validate configuration
if not VERIFY_TOKEN:
    logger.error("WA_VERIFY_TOKEN not set!")
if not ACCESS_TOKEN:
    logger.error("WA_ACCESS_TOKEN not set!")
if not PHONE_NUMBER_ID:
    logger.error("WA_PHONE_NUMBER_ID not set!")


def verify_webhook_signature(payload, signature):
    """Verify that the webhook request came from WhatsApp/Facebook"""
    if not APP_SECRET:
        return True  # Skip verification if secret not configured
    
    expected_signature = hmac.new(
        APP_SECRET.encode('utf-8'),
        payload,
        hashlib.sha256
    ).hexdigest()
    
    return hmac.compare_digest(f"sha256={expected_signature}", signature)


def send_whatsapp_message(recipient_phone, message_text):
    """
    Send a text message via WhatsApp Business API
    
    Args:
        recipient_phone: Phone number in international format (e.g., "1234567890")
        message_text: Message text to send
    
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        if not PHONE_NUMBER_ID or not ACCESS_TOKEN:
            logger.error("WhatsApp credentials not configured!")
            return False
        
        url = f"https://graph.facebook.com/v18.0/{PHONE_NUMBER_ID}/messages"
        
        headers = {
            "Authorization": f"Bearer {ACCESS_TOKEN}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": recipient_phone,
            "type": "text",
            "text": {
                "preview_url": False,
                "body": message_text
            }
        }
        
        response = requests.post(url, json=payload, headers=headers, timeout=10)
        response.raise_for_status()
        
        result = response.json()
        logger.info(f"WhatsApp message sent successfully to {recipient_phone}: {result}")
        return True
        
    except Exception as e:
        logger.error(f"Error sending WhatsApp message: {e}")
        if hasattr(e, 'response') and e.response is not None:
            logger.error(f"Response: {e.response.text}")
        return False


def send_whatsapp_template(recipient_phone, template_name, language_code="en", parameters=None):
    """
    Send a WhatsApp template message (for notifications/reports)
    
    Args:
        recipient_phone: Phone number in international format
        template_name: Name of the approved template
        language_code: Language code (default: "en")
        parameters: List of parameter values for the template
    
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        if not PHONE_NUMBER_ID or not ACCESS_TOKEN:
            logger.error("WhatsApp credentials not configured!")
            return False
        
        url = f"https://graph.facebook.com/v18.0/{PHONE_NUMBER_ID}/messages"
        
        headers = {
            "Authorization": f"Bearer {ACCESS_TOKEN}",
            "Content-Type": "application/json"
        }
        
        template_components = []
        if parameters:
            template_components.append({
                "type": "body",
                "parameters": [{"type": "text", "text": param} for param in parameters]
            })
        
        payload = {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": recipient_phone,
            "type": "template",
            "template": {
                "name": template_name,
                "language": {
                    "code": language_code
                },
                "components": template_components
            }
        }
        
        response = requests.post(url, json=payload, headers=headers, timeout=10)
        response.raise_for_status()
        
        result = response.json()
        logger.info(f"WhatsApp template sent successfully to {recipient_phone}: {result}")
        return True
        
    except Exception as e:
        logger.error(f"Error sending WhatsApp template: {e}")
        if hasattr(e, 'response') and e.response is not None:
            logger.error(f"Response: {e.response.text}")
        return False


def mark_message_as_read(message_id):
    """Mark a WhatsApp message as read"""
    try:
        url = f"https://graph.facebook.com/v18.0/{PHONE_NUMBER_ID}/messages"
        
        headers = {
            "Authorization": f"Bearer {ACCESS_TOKEN}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "messaging_product": "whatsapp",
            "status": "read",
            "message_id": message_id
        }
        
        response = requests.post(url, json=payload, headers=headers, timeout=5)
        response.raise_for_status()
        
        logger.info(f"Message {message_id} marked as read")
        return True
        
    except Exception as e:
        logger.error(f"Error marking message as read: {e}")
        return False


def forward_to_rasa(sender_phone, message_text):
    """Forward message to Rasa and send responses back"""
    try:
        logger.info(f"Forwarding to Rasa from {sender_phone}: {message_text}")
        
        payload = {
            "sender": f"whatsapp_{sender_phone}",
            "message": message_text,
            "metadata": {
                "platform": "whatsapp",
                "source": "whatsapp",
                "phone": sender_phone
            }
        }
        
        response = requests.post(RASA_URL, json=payload, timeout=10)
        response.raise_for_status()
        
        rasa_responses = response.json()
        logger.info(f"Received {len(rasa_responses)} responses from Rasa")
        
        # Send each response back to user
        for rasa_msg in rasa_responses:
            if "text" in rasa_msg:
                send_whatsapp_message(sender_phone, rasa_msg["text"])
                # Note: WhatsApp buttons work differently - would need interactive messages
            elif "image" in rasa_msg:
                # TODO: Implement image sending
                logger.info(f"Image response not yet implemented: {rasa_msg['image']}")
        
        return True
        
    except Exception as e:
        logger.error(f"Error forwarding to Rasa: {e}")
        send_whatsapp_message(sender_phone, "⚠️ Sorry, I'm having trouble processing your message right now.")
        return False


@app.route('/webhooks/whatsapp/webhook', methods=['GET', 'POST'])
def whatsapp_webhook():
    """Handle WhatsApp webhook requests"""
    
    if request.method == 'GET':
        # Webhook verification
        mode = request.args.get('hub.mode')
        token = request.args.get('hub.verify_token')
        challenge = request.args.get('hub.challenge')
        
        if mode == 'subscribe' and token == VERIFY_TOKEN:
            logger.info("WhatsApp webhook verified successfully!")
            return challenge, 200
        else:
            logger.warning("WhatsApp webhook verification failed!")
            return 'Verification failed', 403
    
    elif request.method == 'POST':
        # Verify signature (optional but recommended)
        signature = request.headers.get('X-Hub-Signature-256', '')
        if APP_SECRET and not verify_webhook_signature(request.data, signature):
            logger.warning("Invalid webhook signature!")
            return 'Invalid signature', 403
        
        # Process webhook data
        data = request.json
        logger.debug(f"Received webhook: {data}")
        
        if data.get('object') == 'whatsapp_business_account':
            for entry in data.get('entry', []):
                for change in entry.get('changes', []):
                    value = change.get('value', {})
                    
                    # Handle incoming messages
                    if 'messages' in value:
                        for message in value['messages']:
                            message_id = message.get('id')
                            from_phone = message.get('from')
                            message_type = message.get('type')
                            
                            # Mark message as read
                            if message_id:
                                mark_message_as_read(message_id)
                            
                            # Handle text messages
                            if message_type == 'text':
                                text = message.get('text', {}).get('body', '')
                                if text:
                                    forward_to_rasa(from_phone, text)
                            
                            # Handle button replies
                            elif message_type == 'button':
                                button_text = message.get('button', {}).get('text', '')
                                if button_text:
                                    forward_to_rasa(from_phone, button_text)
                            
                            # Handle interactive replies
                            elif message_type == 'interactive':
                                interactive = message.get('interactive', {})
                                if 'button_reply' in interactive:
                                    button_text = interactive['button_reply'].get('title', '')
                                    forward_to_rasa(from_phone, button_text)
                                elif 'list_reply' in interactive:
                                    list_text = interactive['list_reply'].get('title', '')
                                    forward_to_rasa(from_phone, list_text)
                            
                            # Handle other message types
                            else:
                                send_whatsapp_message(from_phone, "I can only process text messages at the moment.")
                    
                    # Handle status updates (optional)
                    if 'statuses' in value:
                        for status in value['statuses']:
                            logger.debug(f"Message status: {status}")
        
        return 'OK', 200


@app.route('/whatsapp/send', methods=['POST'])
def send_message_api():
    """
    API endpoint to send WhatsApp messages (for reports/notifications)
    
    POST body format:
    {
        "phone": "1234567890",
        "message": "Your report text here"
    }
    """
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
        logger.error(f"Error in send_message_api: {e}")
        return jsonify({"error": str(e)}), 500


@app.route('/whatsapp/send-template', methods=['POST'])
def send_template_api():
    """
    API endpoint to send WhatsApp template messages
    
    POST body format:
    {
        "phone": "1234567890",
        "template": "report_notification",
        "language": "en",
        "parameters": ["param1", "param2"]
    }
    """
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
        logger.error(f"Error in send_template_api: {e}")
        return jsonify({"error": str(e)}), 500


@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "service": "whatsapp_connector",
        "rasa_url": RASA_URL,
        "phone_number_id": PHONE_NUMBER_ID if PHONE_NUMBER_ID else "not_configured"
    }), 200


if __name__ == '__main__':
    logger.info("Starting WhatsApp Webhook Server...")
    logger.info(f"Rasa URL: {RASA_URL}")
    logger.info(f"Verify Token configured: {bool(VERIFY_TOKEN)}")
    logger.info(f"Access Token configured: {bool(ACCESS_TOKEN)}")
    logger.info(f"Phone Number ID configured: {bool(PHONE_NUMBER_ID)}")
    
    # Run Flask app
    app.run(host='0.0.0.0', port=5001, debug=False)
