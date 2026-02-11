# 🚀 Quick Start: Connect Facebook, Instagram & WhatsApp

## What's Been Done ✅

Your project now has:
1. ✅ **Unified webhook handler** (`social_media_webhook.py`) that handles:
   - Facebook Messenger
   - Instagram DMs
   - WhatsApp (receive & send messages)
2. ✅ Docker configuration (single service on port 5000)
3. ✅ Environment variables template
4. ✅ WhatsApp report sending API

## What You Need To Do Next 📋

### Step 1: Get Your Tokens from Facebook (10-15 minutes)

Go to: https://developers.facebook.com/apps/955336886822608

**For Messenger & Instagram:**
1. Add "Messenger" product
2. Add "Instagram" product
3. Generate Page Access Token → Copy it!

**For WhatsApp:**
1. Add "WhatsApp" product
2. Get your Phone Number ID
3. Get your Access Token

> **Detailed instructions:** See `FACEBOOK_INSTAGRAM_WHATSAPP_SETUP.md`

---

### Step 2: Update Your .env File (2 minutes)

Open `.env` and replace these placeholder values:

```bash
# Find these lines and update them:
FB_PAGE_ACCESS_TOKEN=YOUR_PAGE_ACCESS_TOKEN_HERE    # ← Replace this
WA_ACCESS_TOKEN=YOUR_WHATSAPP_ACCESS_TOKEN_HERE     # ← Replace this
WA_PHONE_NUMBER_ID=YOUR_PHONE_NUMBER_ID_HERE        # ← Replace this
```

The verify tokens are already set:
- `FB_VERIFY_TOKEN=vera_fb_verify_2024` ✅
- `WA_VERIFY_TOKEN=vera_wa_verify_2024` ✅

---

### Step 3: Configure Dokploy Domain (5 minutes)

Add routing for the unified webhook service:

**Social Media Webhook Service**
- Host: `selmedia.net`
- Path: `/webhooks` (or `/`)
- Container Port: `5000`
- HTTPS: ✅
- Strip Path: ❌ Disabled

**OR simply expose port 5000:**
- Map host port 5000 → container port 5000
- Then use: `https://selmedia.net:5000/webhooks/...`

**All platforms use the same service on port 5000!** ✨

---

### Step 4: Deploy (5 minutes)

```bash
# Push to git
git add .
git commit -m "Add social media integration"
git push origin main

# Dokploy will auto-deploy
# Or trigger manually in Dokploy dashboard
```

---

### Step 5: Configure Webhooks in Facebook (5 minutes)

Back in Facebook Developer Console:

**Messenger Webhooks:**
- URL: `https://selmedia.net/webhooks/facebook/webhook`
- Verify Token: `vera_fb_verify_2024`
- Click "Verify and Save"
- Subscribe to: `messages`, `messaging_postbacks`

**Instagram Webhooks:**
- URL: `https://selmedia.net/webhooks/facebook/webhook` (same!)
- Verify Token: `vera_fb_verify_2024`
- Subscribe to: `messages`, `messaging_postbacks`

**WhatsApp Webhooks:**
- URL: `https://selmedia.net/webhooks/whatsapp/webhook`
- Verify Token: `vera_wa_verify_2024`
- Subscribe to: `messages`

---

### Step 6: Test! (2 minutes)

**Test Facebook:**
- Message your Facebook Page
- Bot should resp


**Test Instagram:**
- DM your Instagram business account
- Bot should respond!

**Test WhatsApp:**
- Message your WhatsApp business number
- Bot should respond!

**Test WhatsApp Reports (API):**
```bash
curl -X POST https://selmedia.net/whatsapp/send \
  -H "Content-Type: application/json" \
  -d '{"phone": "1234567890", "message": "Test report!"}'
```

---

## 🆘 Troubleshooting

### Webhooks won't verify?
1. Check service is running: `docker-compose ps`
2. Check logs: `docker-compose logs social_media_webhook`
3. Test URL: `curl https://selmedia.net/webhooks/facebook/webhook`

### Messages not working?
1. Verify tokens in `.env` are correct
2. Check webhook subscriptions in Facebook console
3. Check logs: `docker-compose logs -f social_media_webhook`

### Need more help?
See the full guide: `FACEBOOK_INSTAGRAM_WHATSAPP_SETUP.md`

---

## 📁 Files Created

- `social_media_webhook.py` - **Unified webhook handler** for all platforms
- `.env` - Updated with new configuration (update tokens!)
- `docker-compose.yml` - Added unified webhook service (port 5000)
- `requirements.txt` - Added Flask dependency
- `FACEBOOK_INSTAGRAM_WHATSAPP_SETUP.md` - Detailed setup guide

---

## 💡 Quick Tips

1. **One service for all:** Single webhook handles Facebook, Instagram, AND WhatsApp
2. **Same token for FB/IG:** Instagram uses the same Page Access Token as Messenger
3. **Test mode first:** Use Facebook's test numbers before going live
4. **Templates required:** WhatsApp requires approved templates for notifications
5. **Check logs often:** Use `docker-compose logs -f social_media_webhook` to debug
6. **HTTPS required:** All webhooks must use HTTPS (you have it with selmedia.net ✅)

---

## 📱 Sending WhatsApp Reports from Your Code

Add this to your Rasa actions:

```python
import requests

def send_whatsapp_report(phone, message):
    url = "http://social_media_webhook:5000/whatsapp/send"
    response = requests.post(url, json={"phone": phone, "message": message})
    return response.status_code == 200
```

---

## ⏱️ Total Time: ~30-40 minutes

Break it down:
- 10-15 min: Facebook console setup
- 5 min: Update .env
- 5 min: Configure Dokploy
- 5 min: Deploy
- 5 min: Configure webhooks
- 2 min: Testing

**You're almost there! Just follow the steps above and you'll be live! 🎉**
