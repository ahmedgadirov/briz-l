# 🚀 Routing & Webhook Configuration Guide

## ✅ Current Setup Summary

### DNS Configuration (Cloudflare)
```
selmedia.net.    1    IN    A    216.24.57.1 ; cf_tags=cf-proxied:true
```
✅ **No DNS changes needed** - Your DNS is correctly configured!

---

## 🔀 Dokploy Routing Configuration

You have **TWO domain configurations** on the same host:

### Configuration #1: Main Rasa Service
```
Host:           selmedia.net
Path:           /
Container Port: 3000
Service:        rasa
HTTPS:          ✅ Enabled (Let's Encrypt)
```
**Purpose:** Handles all general traffic and Rasa API requests

### Configuration #2: Social Media Webhooks (NEW)
```
Host:           selmedia.net
Path:           /webhooks
Container Port: 5000
Service:        social_media_webhook
HTTPS:          ✅ Enabled (Let's Encrypt)
Strip Path:     ❌ No (keep /webhooks in path)
```
**Purpose:** Handles Facebook, Instagram, and WhatsApp webhook callbacks

---

## 🧪 Testing Your Setup

### 1. Test Health Check Endpoint
```bash
curl https://selmedia.net/health
```

**Expected Response:**
```json
{
  "status": "healthy",
  "service": "social_media_webhook",
  "rasa_url": "http://rasa:3000/webhooks/rest/webhook",
  "facebook_configured": false,
  "whatsapp_configured": false
}
```

### 2. Test Facebook Webhook Verification Endpoint
```bash
curl "https://selmedia.net/webhooks/facebook/webhook?hub.mode=subscribe&hub.verify_token=vera_fb_verify_2024&hub.challenge=test123"
```

**Expected Response:**
```
test123
```
(Your verify token echoed back means it's working!)

### 3. Test WhatsApp Webhook Verification Endpoint
```bash
curl "https://selmedia.net/webhooks/whatsapp/webhook?hub.mode=subscribe&hub.verify_token=vera_wa_verify_2024&hub.challenge=test456"
```

**Expected Response:**
```
test456
```

### 4. Test Rasa Service (should still work)
```bash
curl https://selmedia.net/webhooks/rest/webhook \
  -H "Content-Type: application/json" \
  -d '{"sender":"test","message":"hello"}'
```

---

## 📱 Webhook URLs for Facebook Developer Console

### Facebook Messenger & Instagram Configuration

**Callback URL:**
```
https://selmedia.net/webhooks/facebook/webhook
```

**Verify Token:**
```
vera_fb_verify_2024
```

**Required Webhook Fields:**
- ☑️ messages
- ☑️ messaging_postbacks
- ☑️ message_deliveries (optional)
- ☑️ message_reads (optional)

---

### WhatsApp Business API Configuration

**Callback URL:**
```
https://selmedia.net/webhooks/whatsapp/webhook
```

**Verify Token:**
```
vera_wa_verify_2024
```

**Required Webhook Fields:**
- ☑️ messages

---

## 🔐 Security Configuration

### Environment Variables Required

Update your `.env` file with these values from Facebook Developer Console:

```bash
# Facebook & Instagram
FB_VERIFY_TOKEN=vera_fb_verify_2024
FB_PAGE_ACCESS_TOKEN=your_page_access_token_here
FB_APP_SECRET=your_app_secret_here

# WhatsApp
WA_VERIFY_TOKEN=vera_wa_verify_2024
WA_ACCESS_TOKEN=your_whatsapp_access_token_here
WA_PHONE_NUMBER_ID=your_phone_number_id_here
```

### Where to Find These Tokens

1. **Go to:** https://developers.facebook.com/apps/955336886822608

2. **FB_PAGE_ACCESS_TOKEN:**
   - Messenger Settings → Access Tokens → Generate Token

3. **FB_APP_SECRET:**
   - Settings → Basic → App Secret (click Show)

4. **WA_ACCESS_TOKEN & WA_PHONE_NUMBER_ID:**
   - WhatsApp → API Setup
   - Temporary Access Token (later get permanent one)
   - Phone Number ID

---

## 🚀 Deployment Steps

### 1. Update Environment Variables
```bash
# Edit .env file with your tokens
nano .env
```

### 2. Rebuild and Deploy
```bash
# Push to Git (Dokploy will auto-deploy)
git add .env
git commit -m "Update social media tokens"
git push origin main
```

Or manually trigger deployment in Dokploy dashboard.

### 3. Verify Services are Running
```bash
# Check Docker containers
docker ps | grep rasa
```

You should see:
- `rasa` container on port 3001→3000
- `social_media_webhook` container on port 5000→5000
- `action_server` container on port 5055
- `telegram_poller` container

### 4. Test Webhook Endpoints
Run the curl commands from the "Testing Your Setup" section above.

### 5. Configure Facebook/WhatsApp Webhooks
- Log into Facebook Developer Console
- Add webhook URLs and verify tokens
- Subscribe to required events

---

## 🔍 Troubleshooting

### Issue: Health check returns 404
**Solution:** Make sure port 5000 container is running
```bash
docker logs rasa-brizl-social_media_webhook-1
```

### Issue: Webhook verification fails
**Possible causes:**
1. Wrong verify token in .env file
2. Service not running on port 5000
3. Dokploy routing not configured correctly
4. SSL certificate not active

**Check logs:**
```bash
docker logs -f rasa-brizl-social_media_webhook-1
```

### Issue: Messages not reaching Rasa
**Check:**
1. Verify Rasa is running: `curl http://localhost:3001/version`
2. Check environment variable `RASA_URL=http://rasa:3000/webhooks/rest/webhook`
3. Check Docker network connectivity

### Issue: Facebook says "Invalid token"
**Solution:** 
1. Verify tokens in .env match Facebook Developer Console
2. Restart social_media_webhook service after updating .env
3. Check that tokens don't have extra spaces

---

## 📊 Service Architecture

```
Internet
   ↓
Cloudflare Proxy (216.24.57.1)
   ↓
selmedia.net (HTTPS)
   ↓
Dokploy Reverse Proxy
   ├─→ /webhooks/* → Port 5000 (social_media_webhook)
   │   ├─→ /webhooks/facebook/webhook (Facebook & Instagram)
   │   ├─→ /webhooks/whatsapp/webhook (WhatsApp)
   │   └─→ /health (Health check)
   │
   └─→ /* → Port 3000 (Rasa)
       └─→ /webhooks/rest/webhook (Rasa API)

Docker Network (dokploy-network)
   ├─ rasa (port 3000)
   ├─ social_media_webhook (port 5000) → talks to rasa
   ├─ action_server (port 5055) ← called by rasa
   └─ telegram_poller → talks to rasa
```

---

## ✅ Verification Checklist

- [ ] Health endpoint responds: `curl https://selmedia.net/health`
- [ ] Facebook webhook verifies: Returns challenge token
- [ ] WhatsApp webhook verifies: Returns challenge token
- [ ] Rasa endpoint still works: `curl https://selmedia.net/webhooks/rest/webhook`
- [ ] Environment variables updated in `.env`
- [ ] Services redeployed with new .env
- [ ] Facebook Developer Console webhooks configured
- [ ] WhatsApp Business API webhooks configured
- [ ] Test message from Facebook Messenger → receives response
- [ ] Test message from Instagram DM → receives response
- [ ] Test message from WhatsApp → receives response

---

## 🎉 Next Steps

1. **Test the health endpoint** to confirm routing works
2. **Update .env** with your Facebook/WhatsApp tokens
3. **Redeploy** the services
4. **Configure webhooks** in Facebook Developer Console
5. **Send test messages** from each platform
6. **Monitor logs** to ensure everything works

---

## 📞 Support

If you encounter issues:
1. Check Docker logs: `docker logs -f rasa-brizl-social_media_webhook-1`
2. Verify routing in Dokploy dashboard
3. Test with curl commands above
4. Check Facebook Developer Console for webhook status

Good luck! 🚀
