# Facebook Messenger, Instagram & WhatsApp Integration Setup Guide

This guide walks you through connecting your Rasa chatbot to Facebook Messenger, Instagram DMs, and WhatsApp Business API.

## 📋 Prerequisites

Before starting, ensure you have:
- ✅ Facebook Developer Account
- ✅ Facebook App ID: `955336886822608`
- ✅ Facebook App Secret: `bdca1c29634daaf56f66972696286a1a`
- ✅ A Facebook Page (required for Messenger)
- ✅ Instagram Business Account (connected to your Facebook Page)
- ✅ WhatsApp Business Account or phone number
- ✅ Domain with HTTPS: `selmedia.net`

---

## 🚀 Part 1: Facebook Developer Console Setup

### Step 1: Add Messenger Product

1. Go to [Facebook Developer Console](https://developers.facebook.com/apps/955336886822608/dashboard/)
2. Click **"Add Product"** in the left sidebar
3. Find **"Messenger"** → Click **"Set Up"**

### Step 2: Configure Messenger Webhooks

1. In Messenger Settings, scroll to **"Webhooks"** section
2. Click **"Add Callback URL"**
3. Enter the following:
   - **Callback URL:** `https://selmedia.net/webhooks/facebook/webhook`
   - **Verify Token:** `vera_fb_verify_2024`
   - Click **"Verify and Save"**

4. Subscribe to webhook fields:
   - ✅ `messages`
   - ✅ `messaging_postbacks`
   - ✅ `message_reads`
   - ✅ `message_deliveries`

### Step 3: Generate Page Access Token

1. In Messenger Settings → **"Access Tokens"** section
2. Select your Facebook Page (or create one if needed)
3. Click **"Generate Token"**
4. **Copy the token** - you'll need this later!
5. Save it to `.env` file as `FB_PAGE_ACCESS_TOKEN`

### Step 4: Add Instagram Messaging Product

1. Click **"Add Product"** → Find **"Instagram"**
2. Click **"Set Up"**
3. Follow the wizard to connect your Instagram Business Account
4. In Instagram Settings → **"Webhooks"**:
   - The webhook URL is the same: `https://selmedia.net/webhooks/facebook/webhook`
   - Subscribe to: `messages`, `messaging_postbacks`

**Note:** Instagram uses the same Page Access Token as Messenger!

### Step 5: Add WhatsApp Product

1. Click **"Add Product"** → Find **"WhatsApp"**
2. Click **"Set Up"**
3. Follow the setup wizard:
   - Add a phone number (or use test number for development)
   - Verify your business
   - Complete the setup

4. Get your credentials:
   - **Phone Number ID:** Found in WhatsApp → API Setup
   - **Access Token:** Generated in WhatsApp → API Setup
   - **Copy these values!**

5. Configure WhatsApp Webhooks:
   - **Callback URL:** `https://selmedia.net/webhooks/whatsapp/webhook`
   - **Verify Token:** `vera_wa_verify_2024`
   - Subscribe to: `messages`

---

## 🔧 Part 2: Configure Your Environment

### Step 1: Update `.env` File

Open `/Users/bytelecom/Desktop/rasa-brizl/.env` and update these values:

```bash
# Facebook/Instagram Configuration
FB_VERIFY_TOKEN=vera_fb_verify_2024
FB_PAGE_ACCESS_TOKEN=PASTE_YOUR_PAGE_ACCESS_TOKEN_HERE
FB_APP_SECRET=bdca1c29634daaf56f66972696286a1a

# WhatsApp Configuration
WA_VERIFY_TOKEN=vera_wa_verify_2024
WA_ACCESS_TOKEN=PASTE_YOUR_WHATSAPP_ACCESS_TOKEN_HERE
WA_PHONE_NUMBER_ID=PASTE_YOUR_PHONE_NUMBER_ID_HERE
```

**Where to find these values:**
- **FB_PAGE_ACCESS_TOKEN:** From Step 3 above (Messenger Settings → Access Tokens)
- **WA_ACCESS_TOKEN:** From Step 5 above (WhatsApp → API Setup)
- **WA_PHONE_NUMBER_ID:** From Step 5 above (WhatsApp → API Setup)

---

## 📦 Part 3: Dokploy Configuration

### Configure Domain Routing

You need to configure **THREE** services in Dokploy:

#### 1. Main Rasa Service (Already configured)
- **Host:** `selmedia.net`
- **Path:** `/`
- **Container Port:** `3000`
- **HTTPS:** ✅ Enabled

#### 2. Facebook/Instagram Webhook Service (NEW)
- **Host:** `selmedia.net`
- **Path:** `/webhooks/facebook/*`
- **Container Port:** `5000`
- **HTTPS:** ✅ Enabled
- **Strip Path:** ❌ Disabled

#### 3. WhatsApp Webhook Service (NEW)
- **Host:** `selmedia.net`
- **Path:** `/webhooks/whatsapp/*`
- **Container Port:** `5001`
- **HTTPS:** ✅ Enabled
- **Strip Path:** ❌ Disabled

### Alternative: Use a Reverse Proxy

If Dokploy doesn't support path-based routing, you can configure all webhook services through the main Rasa container or use nginx:

```nginx
location /webhooks/facebook/ {
    proxy_pass http://facebook_instagram_webhook:5000;
}

location /webhooks/whatsapp/ {
    proxy_pass http://whatsapp_webhook:5001;
}
```

---

## 🏗️ Part 4: Build and Deploy

### Step 1: Rebuild Docker Images

```bash
cd /Users/bytelecom/Desktop/rasa-brizl

# Rebuild the main image (includes new webhook scripts)
docker-compose build rasa

# Or rebuild all services
docker-compose build
```

### Step 2: Deploy to Dokploy

```bash
# Push changes to git
git add .
git commit -m "Add Facebook, Instagram, and WhatsApp integration"
git push origin main

# Dokploy should auto-deploy, or trigger manually in Dokploy dashboard
```

### Step 3: Start Services

```bash
# If testing locally first:
docker-compose up -d

# Check logs
docker-compose logs -f facebook_instagram_webhook
docker-compose logs -f whatsapp_webhook
```

---

## ✅ Part 5: Testing

### Test Facebook Messenger

1. Go to your Facebook Page
2. Click **"Message"** button
3. Send a test message
4. Your bot should respond!

### Test Instagram

1. Open Instagram app
2. Go to your business account's profile
3. Send a DM to yourself (or have someone else send)
4. Bot should respond!

### Test WhatsApp

1. Add your test phone number in Facebook Developer Console (WhatsApp → Configuration)
2. Send a message from WhatsApp to your business number
3. Bot should respond!

### Test WhatsApp Report Sending

You can send reports programmatically using the API:

```bash
# Send a text message
curl -X POST https://selmedia.net/whatsapp/send \
  -H "Content-Type: application/json" \
  -d '{
    "phone": "1234567890",
    "message": "Your medical report is ready!"
  }'

# Send a template message (requires approved template)
curl -X POST https://selmedia.net/whatsapp/send-template \
  -H "Content-Type: application/json" \
  -d '{
    "phone": "1234567890",
    "template": "report_notification",
    "language": "en",
    "parameters": ["Patient Name", "Report Date"]
  }'
```

---

## 🔍 Troubleshooting

### Webhook Verification Failed

**Problem:** Facebook says "Webhook verification failed"

**Solutions:**
1. Ensure services are running: `docker-compose ps`
2. Check logs: `docker-compose logs facebook_instagram_webhook`
3. Verify the URL is accessible: `curl https://selmedia.net/webhooks/facebook/webhook`
4. Verify token must match exactly: `vera_fb_verify_2024`
5. Check Dokploy routing configuration

### Messages Not Being Received

**Problem:** Bot doesn't respond to messages

**Solutions:**
1. Check webhook subscriptions in Facebook Developer Console
2. Verify `.env` has correct tokens
3. Check service logs: `docker-compose logs -f facebook_instagram_webhook`
4. Verify Rasa is running: `docker-compose logs rasa`
5. Test Rasa directly: `curl http://localhost:3001/`

### WhatsApp Not Working

**Problem:** WhatsApp bot not responding or returning 400 error

**Solutions:**
1. Verify WhatsApp credentials in `.env`
2. Check if phone number is verified in Facebook console
3. **Display Name Approval**: If logs show error `#131037`, you need to set or wait for display name approval in the WhatsApp Manager.
4. Ensure webhook is subscribed to `messages` field
5. Check logs: `docker-compose logs whatsapp_webhook`
6. Test the WhatsApp API directly using Graph API Explorer

### 403 Forbidden / Signature Verification Failed

**Problem:** Webhook returns 403 error

**Solutions:**
1. Verify `FB_APP_SECRET` in `.env` is correct
2. Check signature verification in logs
3. Temporarily disable signature check for testing (not recommended for production)

---

## 📱 Using Rasa Actions to Send WhatsApp Reports

You can integrate WhatsApp messaging into your Rasa custom actions:

```python
# In actions/response_generator.py or any custom action

import os
import requests

def send_whatsapp_report(phone_number, report_text):
    """Send a WhatsApp report from within a Rasa action"""
    whatsapp_api_url = os.getenv("WHATSAPP_SERVICE_URL", "http://whatsapp_webhook:5001/whatsapp/send")
    
    payload = {
        "phone": phone_number,
        "message": report_text
    }
    
    try:
        response = requests.post(whatsapp_api_url, json=payload, timeout=10)
        response.raise_for_status()
        return True
    except Exception as e:
        print(f"Error sending WhatsApp message: {e}")
        return False

# Example usage in a custom action
class ActionSendReport(Action):
    def name(self) -> Text:
        return "action_send_report"
    
    def run(self, dispatcher, tracker, domain):
        # Get user phone from tracker
        phone = tracker.get_slot("phone_number")
        
        if phone:
            report = "Your medical report is ready. Please visit our clinic."
            if send_whatsapp_report(phone, report):
                dispatcher.utter_message(text="Report sent to your WhatsApp!")
            else:
                dispatcher.utter_message(text="Failed to send report.")
        
        return []
```

---

## 🔐 Security Best Practices

1. **Never commit tokens to git:**
   - Ensure `.env` is in `.gitignore`
   - Use environment variables in production

2. **Enable signature verification:**
   - Keep `FB_APP_SECRET` configured
   - Don't disable signature checks in production

3. **Use HTTPS only:**
   - Facebook requires HTTPS for webhooks
   - Ensure SSL certificate is valid

4. **Rotate tokens regularly:**
   - Regenerate access tokens periodically
   - Update `.env` file when rotating

5. **Monitor webhook health:**
   - Check logs regularly
   - Set up alerts for failures

---

## 📊 Monitoring

Check service health:

```bash
# Facebook/Instagram webhook health
curl https://selmedia.net/health

# WhatsApp webhook health  
curl https://selmedia.net/whatsapp/health

# Check all services
docker-compose ps
docker-compose logs --tail=50 -f
```

---

## 🎯 Next Steps

1. **Complete Facebook Developer Console setup** (follow Part 1)
2. **Get all required tokens** (Page Access Token, WhatsApp tokens)
3. **Update `.env` file** with real tokens
4. **Configure Dokploy routing** for webhook services
5. **Deploy and test** each platform
6. **Create WhatsApp message templates** for report notifications
7. **Integrate WhatsApp sending** into your Rasa actions

---

## 📞 Support

If you encounter issues:

1. Check service logs: `docker-compose logs [service_name]`
2. Verify webhook configuration in Facebook Developer Console
3. Test webhooks using Facebook's Webhook Test Tool
4. Check Dokploy routing and SSL configuration
5. Verify all tokens are correct in `.env`

---

## 📝 Summary

**Webhook URLs:**
- Facebook/Instagram: `https://selmedia.net/webhooks/facebook/webhook`
- WhatsApp: `https://selmedia.net/webhooks/whatsapp/webhook`

**Verify Tokens:**
- Facebook/Instagram: `vera_fb_verify_2024`
- WhatsApp: `vera_wa_verify_2024`

**Services:**
- Port 5000: Facebook/Instagram webhook handler
- Port 5001: WhatsApp webhook handler + report sender
- Port 3000: Main Rasa server

Good luck with your integration! 🚀
