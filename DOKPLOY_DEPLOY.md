# Dokploy Deployment Quick Start

This is a quick reference for deploying the Rasa bot to Dokploy as a Compose stack.

## ⚡ Quick Deploy

### 1. Create Compose Application in Dokploy
- Application Type: **Compose** (NOT Docker/Application)
- Name: `rasa-brizl`
- Repository: `https://github.com/ahmedgadirov/briz-l.git`
- Branch: `main`
- Compose File: `docker-compose.yml`

### 2. Set Environment Variables

Copy these variables into Dokploy's environment configuration (replace with your actual values):

```bash
TELEGRAM_BOT_TOKEN=<your_telegram_bot_token_from_botfather>
OPENAI_API_KEY=<your_openai_api_key>
DB_PASSWORD=herahera
PYTHONWARNINGS=ignore
SQLALCHEMY_SILENCE_UBER_WARNING=1
```

> **Note:** Get your actual values from the `.env` file in the repository.


### 3. Deploy & Verify

1. Click **Deploy** in Dokploy
2. Wait for build to complete (3-5 minutes)
3. Check logs for all 3 services:
   - ✅ `rasa`: "Rasa server is up and running"
   - ✅ `action_server`: "Action server is up and running"
   - ✅ `telegram_poller`: "Successfully connected to Rasa server!"

### 4. Test Bot

1. Open Telegram
2. Send: `salam`
3. **Expected:** Greeting menu appears with buttons
4. Click: "❓ Sual ver"
5. Send: `necesen`
6. **Expected:** AI-generated response (no action server error)

## 🔧 Troubleshooting

### ❌ "Cannot connect to host action_server:5055"
**Solution:** You deployed services individually. Delete them and create a **Compose** application instead.

### ❌ "409 Conflict: terminated by other getUpdates"
**Solution:** Multiple bot instances running. Delete old deployments.

### ❌ Database connection error
**Solution:** Verify database `rasa-brizl-tbycs9` is running and password matches.

## 📚 Full Documentation

See [dokploy-deployment-guide.md](file:///Users/bytelecom/.gemini/antigravity/brain/8070d288-281e-4fd7-835a-fec0fe6d3b8c/dokploy-deployment-guide.md) for detailed instructions.
