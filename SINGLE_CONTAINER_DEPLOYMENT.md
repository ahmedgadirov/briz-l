# 🚀 Single Container Deployment Guide

## ✅ What Was Updated

I've configured your project to run **ALL services in ONE Docker container**:

### Services Running in Single Container:
1. **Rasa Server** → Port 3000
2. **Action Server** → Port 5055
3. **Social Media Webhook** → Port 5000 (Facebook/Instagram/WhatsApp)
4. **Telegram Poller** → Background process

---

## 📝 Files Updated

### 1. `start.sh` ✅
Added Social Media Webhook server to startup sequence:
```bash
- Starts Rasa Action Server (port 5055)
- Starts Rasa Server (port 3000)
- Starts Social Media Webhook (port 5000) ← NEW!
- Starts Telegram Poller
```

### 2. `Dockerfile` ✅
Added port 5000 exposure:
```dockerfile
EXPOSE 3000 5000 5055
```

### 3. `.env` ✅
Added RASA_URL for internal communication:
```bash
RASA_URL=http://localhost:3000/webhooks/rest/webhook
```

---

## 🔧 Dokploy Configuration

Since you're using ONE container, you need to configure Dokploy to expose **TWO ports**:

### Port Mappings Required:

#### Main Application Port:
```
Container Port: 3000
Exposed Port:   3000 (or auto)
Service:        Rasa API
```

#### Webhook Port:
```
Container Port: 5000
Exposed Port:   5000 (or auto)
Service:        Social Media Webhooks
```

### Domain Routing in Dokploy:

#### Domain #1: Main Traffic (Rasa)
```
Host:           selmedia.net
Path:           /
Container Port: 3000
HTTPS:          ✅ Enabled
```

#### Domain #2: Webhook Traffic
```
Host:           selmedia.net
Path:           /webhooks
Container Port: 5000
HTTPS:          ✅ Enabled
Strip Path:     NO
```

**OR use subdomain:**
```
Host:           webhooks.selmedia.net
Path:           /
Container Port: 5000
HTTPS:          ✅ Enabled
```

---

## 🚀 Deployment Steps

### Step 1: Commit and Push Changes
```bash
git add .
git commit -m "Add social media webhook to single container"
git push origin main
```

### Step 2: Rebuild in Dokploy
1. Go to Dokploy dashboard
2. Find your `rasa-brizl` application
3. Click "Rebuild" or trigger a new deployment
4. Wait for build to complete (2-5 minutes)

### Step 3: Configure Port Mappings
In Dokploy, make sure these ports are mapped:
- Port 3000 → for Rasa
- Port 5000 → for Webhooks

### Step 4: Configure Domain Routing
Add two domain configurations:
- `selmedia.net/` → Port 3000
- `selmedia.net/webhooks` → Port 5000

---

## 🧪 Testing After Deployment

### Test 1: Rasa Server
```bash
curl https://selmedia.net/
```
**Expected:** `Hello from Rasa: 3.6.0`

### Test 2: Health Check
```bash
curl https://selmedia.net/health
```
**Expected:**
```json
{
  "status": "healthy",
  "service": "social_media_webhook",
  "rasa_url": "http://localhost:3000/webhooks/rest/webhook",
  "facebook_configured": false,
  "whatsapp_configured": false
}
```

### Test 3: Facebook Webhook Verification
```bash
curl "https://selmedia.net/webhooks/facebook/webhook?hub.mode=subscribe&hub.verify_token=vera_fb_verify_2024&hub.challenge=test123"
```
**Expected:** `test123`

### Test 4: WhatsApp Webhook Verification
```bash
curl "https://selmedia.net/webhooks/whatsapp/webhook?hub.mode=subscribe&hub.verify_token=vera_wa_verify_2024&hub.challenge=test456"
```
**Expected:** `test456`

---

## 📱 Facebook/WhatsApp Configuration

Once deployed and tested, configure webhooks:

### Facebook & Instagram
1. Go to https://developers.facebook.com/apps/955336886822608
2. Add Messenger Product
3. Configure Webhook:
   - **URL:** `https://selmedia.net/webhooks/facebook/webhook`
   - **Verify Token:** `vera_fb_verify_2024`
   - **Subscribe to:** messages, messaging_postbacks

### WhatsApp
1. Add WhatsApp Product
2. Configure Webhook:
   - **URL:** `https://selmedia.net/webhooks/whatsapp/webhook`
   - **Verify Token:** `vera_wa_verify_2024`
   - **Subscribe to:** messages

---

## 🔍 Troubleshooting

### Issue: Port 5000 not accessible
**Solution:**
1. Check Dokploy port mappings - ensure 5000 is exposed
2. Verify domain routing for /webhooks path
3. Check container logs: Look for "Starting Social Media Webhook Server"

### Issue: "Connection refused" to Rasa
**Solution:**
- The webhook service connects to Rasa via `localhost:3000`
- This should work since everything is in same container
- Check logs to see if Rasa started successfully

### Issue: 502 Bad Gateway on /webhooks
**Possible causes:**
1. Port 5000 not exposed in Dokploy
2. Domain routing not configured for /webhooks path
3. Webhook service didn't start (check logs)

### Check Container Logs
```bash
# In Dokploy, view logs to see:
# "Starting Social Media Webhook Server on port 5000..."
# "Starting Rasa Server on port 3000..."
```

---

## 📊 Container Architecture

```
┌─────────────────────────────────────────────────┐
│  Single Docker Container                        │
│                                                  │
│  ┌──────────────────┐                          │
│  │ Rasa Server      │ Port 3000                │
│  │ (Chatbot API)    │                          │
│  └──────────────────┘                          │
│           ↑                                     │
│           │ (localhost)                         │
│           │                                     │
│  ┌──────────────────┐                          │
│  │ Action Server    │ Port 5055                │
│  │ (Custom Actions) │                          │
│  └──────────────────┘                          │
│           ↑                                     │
│           │ (localhost)                         │
│           │                                     │
│  ┌──────────────────┐                          │
│  │ Social Media     │ Port 5000                │
│  │ Webhook Server   │ ← Facebook/WhatsApp      │
│  │ (Flask)          │                          │
│  └──────────────────┘                          │
│           │                                     │
│           ↓ sends to localhost:3000            │
│                                                  │
│  ┌──────────────────┐                          │
│  │ Telegram Poller  │ No port                  │
│  │ (Background)     │                          │
│  └──────────────────┘                          │
└─────────────────────────────────────────────────┘
```

---

## ✅ Deployment Checklist

- [x] Update start.sh with webhook service
- [x] Update Dockerfile to expose port 5000
- [x] Update .env with RASA_URL
- [ ] Commit and push to Git
- [ ] Rebuild in Dokploy
- [ ] Configure port mappings (3000, 5000)
- [ ] Configure domain routing
- [ ] Test health endpoint
- [ ] Test webhook verification
- [ ] Configure Facebook Developer Console
- [ ] Configure WhatsApp Business API
- [ ] Test end-to-end message flow

---

## 🎯 Summary

**Before:** Multiple containers with docker-compose
**After:** Single container with all services

**Advantages:**
- Simpler deployment
- Easier to manage in Dokploy
- All services in one place
- Faster communication between services

**Next Steps:**
1. Push code to Git
2. Rebuild in Dokploy
3. Configure ports and domains
4. Test webhooks
5. Connect to Facebook/Instagram/WhatsApp

🚀 **Ready to deploy!**
