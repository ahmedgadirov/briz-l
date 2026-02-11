# 🔍 Facebook Webhook Verification Troubleshooting

## Current Issue
Your webhook is **responding** (✅ service is running!) but returning "Verification failed" (❌ token mismatch).

## What's Happening

When you curl:
```bash
curl "https://selmedia.net/webhooks/facebook/webhook?hub.mode=subscribe&hub.verify_token=vera_fb_verify_2024&hub.challenge=test123"
```

**Expected Response:** `test123` (the challenge)  
**Actual Response:** `Verification failed`

## Root Cause Analysis

The webhook verification is failing because one of these conditions is not met:

```python
if mode == 'subscribe' and token and FB_VERIFY_TOKEN and token == FB_VERIFY_TOKEN:
    return challenge  # SUCCESS
else:
    return 'Verification failed'  # FAILURE
```

### Possible Issues:

1. **Environment Variable Not Loading** - `.env` file not read by Docker
2. **Token Mismatch** - Typo in environment variable vs curl command
3. **Routing Issue** - Request not reaching the correct service

## 🛠️ Step-by-Step Fix

### Step 1: Test Locally First

1. **Start the webhook server locally:**
   ```bash
   cd /Users/bytelecom/Desktop/rasa-brizl
   python social_media_webhook.py
   ```

2. **Test verification (in another terminal):**
   ```bash
   curl "http://localhost:5000/webhooks/facebook/webhook?hub.mode=subscribe&hub.verify_token=vera_fb_verify_2024&hub.challenge=test123"
   ```

   **Expected output:** `test123`

3. **Check the logs** in the first terminal - you should see:
   ```
   Facebook verification attempt:
     Mode: subscribe
     Received token: vera_fb_verify_2024
     Expected token: vera_fb_verify_2024
     Challenge: test123
   ✅ Facebook/Instagram webhook verified successfully!
   ```

### Step 2: If Local Test Fails

If you see `Expected token: None` in the logs, the `.env` file isn't being read:

```bash
# Option A: Export manually
export FB_VERIFY_TOKEN=vera_fb_verify_2024
export FB_PAGE_ACCESS_TOKEN=YOUR_PAGE_ACCESS_TOKEN_HERE
export FB_APP_SECRET=bdca1c29634daaf56f66972696286a1a
python social_media_webhook.py

# Option B: Load .env explicitly
pip install python-dotenv
```

Then update `social_media_webhook.py` to load `.env`:
```python
from dotenv import load_dotenv
load_dotenv()  # Add this at the top after imports
```

### Step 3: Fix Docker Environment Variables

The issue is that Docker needs environment variables passed explicitly. Update `Dockerfile`:

```dockerfile
# Load environment variables from .env during build
ENV FB_VERIFY_TOKEN=vera_fb_verify_2024
ENV WA_VERIFY_TOKEN=vera_wa_verify_2024
```

**OR** better yet, in Dokploy:

1. Go to your application settings
2. Add Environment Variables:
   - `FB_VERIFY_TOKEN` = `vera_fb_verify_2024`
   - `WA_VERIFY_TOKEN` = `vera_wa_verify_2024`
   - `FB_PAGE_ACCESS_TOKEN` = (your actual token)
   - `FB_APP_SECRET` = `bdca1c29634daaf56f66972696286a1a`

### Step 4: Check Dokploy Logs

After redeploying, check the container logs in Dokploy:

Look for the startup message:
```
Starting Unified Social Media Webhook Server
Facebook/Instagram:
  - Verify Token: True  <-- Must be True!
  - Page Access Token: False
  - App Secret: True
```

If "Verify Token: False" → Environment variable not loaded!

### Step 5: Test the Deployed Webhook

Once deployed with proper environment variables:

```bash
curl "https://selmedia.net/webhooks/facebook/webhook?hub.mode=subscribe&hub.verify_token=vera_fb_verify_2024&hub.challenge=test123"
```

**Expected:** `test123`

## 🔧 Quick Fix Commands

### Option 1: Install python-dotenv (Recommended)

```bash
# Add to requirements.txt
echo "python-dotenv" >> requirements.txt

# Update webhook to load .env
```

### Option 2: Use Environment Variables in Dokploy

Configure in Dokploy dashboard instead of `.env` file:
- Navigate to: Application → Environment Variables
- Add all variables from `.env` file
- Redeploy

## 📊 Debugging Commands

```bash
# Test health endpoint
curl https://selmedia.net/webhooks/health

# Check if service is running
curl https://selmedia.net/webhooks/facebook/webhook

# View Dokploy logs
# (Check in Dokploy dashboard → Logs)
```

## ✅ Success Checklist

- [ ] Local test passes (returns `test123`)
- [ ] Startup logs show `Verify Token: True`
- [ ] Remote test passes (curl to selmedia.net)
- [ ] Facebook Developer Console webhook verification succeeds
- [ ] Test message from Facebook page receives response

## Next Steps After Fix

1. **Commit changes:**
   ```bash
   git add .
   git commit -m "Fix webhook verification with environment variable loading"
   git push origin main
   ```

2. **Configure in Facebook Developer Console:**
   - Callback URL: `https://selmedia.net/webhooks/facebook/webhook`
   - Verify Token: `vera_fb_verify_2024`
   - Subscribe to: `messages`, `messaging_postbacks`

3. **Test end-to-end:**
   - Send message to your Facebook page
   - Verify bot responds through Rasa

## 📝 Notes

- The webhook **IS running** (you got a response)
- The issue is **environment variable loading** in Docker
- Solution: Either use `python-dotenv` OR configure env vars in Dokploy directly
