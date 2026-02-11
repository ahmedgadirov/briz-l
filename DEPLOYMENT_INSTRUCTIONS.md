# 🚀 All-in-One Container Deployment Instructions

## What Changed

Your Rasa bot now runs **all 3 services in a single container**:
- ✅ Rasa Server (port 3000)
- ✅ Action Server (port 5055)
- ✅ Telegram Poller

This simplifies deployment on Dokploy using the **Dockerfile build type**.

---

## Deployment Steps on Dokploy

### 1. Redeploy Your Application

In your Dokploy dashboard:

1. **Go to your `rasa-brizl` application**
2. **Click "Redeploy"** or **"Rebuild"**
   - Dokploy will pull the latest code from GitHub
   - It will rebuild the Docker image with the new startup script
3. **Wait 3-5 minutes** for the build to complete

### 2. Monitor the Logs

After deployment, check the container logs. You should see:

```
🚀 Starting All-in-One Rasa Container...
📦 Starting Rasa Action Server on port 5055...
⏳ Waiting for Action Server to start...
🤖 Starting Rasa Server on port 3000...
⏳ Waiting for Rasa Server to start...
📱 Starting Telegram Poller...
✅ All services started!
   - Action Server: PID xxx (port 5055)
   - Rasa Server: PID xxx (port 3000)
   - Telegram Poller: PID xxx

Starting Telegram Polling Bridge...
Testing connection to Rasa at http://localhost:3000/webhooks/rest/webhook...
Successfully connected to Rasa server! Status: {...}
Polling for Telegram updates...
```

### 3. Test Your Bot

1. Open Telegram
2. Find your bot: **@rasabrizbot**
3. Send: **"salam"**
4. You should get a greeting with menu buttons! 🎉

---

## What to Look For

### ✅ Success Indicators:
- All 3 services start with PID numbers
- "Successfully connected to Rasa server!" message
- "Polling for Telegram updates..." message
- Bot responds in Telegram

### ❌ Common Issues:

**"Could not connect to Rasa server"**
- Action server took too long to start
- Solution: Check if ports 5055/3000 are available

**"409 Conflict: terminated by other getUpdates"**
- Another instance is polling Telegram
- Solution: Stop/delete old deployments

**"Unauthorized" in Telegram logs**
- Wrong bot token
- Solution: Verify TELEGRAM_BOT_TOKEN in Dokploy env vars

**Action server errors**
- Missing environment variables (OPENAI_API_KEY)
- Solution: Add all env vars from .env file to Dokploy

---

## Environment Variables Required

Make sure these are set in Dokploy's Environment Variables section:

```bash
TELEGRAM_BOT_TOKEN=your_telegram_bot_token_here
OPENAI_API_KEY=your_openai_api_key_here
DB_PASSWORD=your_database_password_here
PYTHONWARNINGS=ignore
SQLALCHEMY_SILENCE_UBER_WARNING=1
```

**⚠️ IMPORTANT - Getting Your Tokens:**
- **TELEGRAM_BOT_TOKEN**: Get from [@BotFather](https://t.me/botfather) on Telegram
- **OPENAI_API_KEY**: Get from [OpenAI Platform](https://platform.openai.com/api-keys)
- **Never commit these secrets to Git!** Only set them in:
  - Your local `.env` file (which is gitignored)
  - Dokploy's Environment Variables dashboard

---

## Architecture

**Before (didn't work):**
- 3 separate containers that weren't deployed

**After (works!):**
```
┌─────────────────────────────────────┐
│   Single Container                  │
│                                     │
│  ┌──────────────┐                  │
│  │ Action Server│ (port 5055)      │
│  └──────────────┘                  │
│         ↑                           │
│  ┌──────┴───────┐                  │
│  │ Rasa Server  │ (port 3000)      │
│  └──────────────┘                  │
│         ↑                           │
│  ┌──────┴───────┐                  │
│  │ Telegram     │                  │
│  │ Poller       │ ←→ Telegram API  │
│  └──────────────┘                  │
└─────────────────────────────────────┘
```

---

## Troubleshooting

If something doesn't work:

1. **Check all service logs** in Dokploy
2. **Look for the startup emoji messages** (🚀 📦 🤖 📱)
3. **Verify all 3 PIDs are shown**
4. **Test Telegram bot manually**
5. **Check environment variables are set**

Need help? Share the full container logs!
