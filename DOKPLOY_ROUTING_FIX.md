# 🔧 Dokploy Routing Configuration

## ✅ DNS Fixed! But Routing Needs Configuration

**Current Status:**
- ✅ `https://selmedia.net/` → Works! (Returns "Hello from Rasa: 3.6.0")
- ❌ `https://selmedia.net/webhooks/` → 502 Error (Not reaching port 5000)

---

## 🎯 The Problem

You have **TWO services** that need different routing:

1. **Rasa service** (port 3000) - Main chatbot API
2. **Social Media Webhook** (port 5000) - Facebook/Instagram/WhatsApp webhooks

Currently, ALL traffic goes to port 3000 (Rasa), but `/webhooks/*` paths need to go to port 5000.

---

## 🚀 Dokploy Configuration Required

You need to configure Dokploy to have **TWO domain entries** with different paths:

### Configuration #1: Webhook Service (PRIORITY: HIGH)
```
┌─────────────────────────────────────────────┐
│ Service: social_media_webhook               │
├─────────────────────────────────────────────┤
│ Host:              selmedia.net             │
│ Path:              /webhooks                │
│ Container Port:    5000                     │
│ HTTPS:             ✅ Enabled               │
│ Strip Path:        NO (keep /webhooks)      │
│ Priority:          HIGHER (match first)     │
└─────────────────────────────────────────────┘
```

### Configuration #2: Main Rasa Service (PRIORITY: LOWER)
```
┌─────────────────────────────────────────────┐
│ Service: rasa                               │
├─────────────────────────────────────────────┤
│ Host:              selmedia.net             │
│ Path:              /                        │
│ Container Port:    3000                     │
│ HTTPS:             ✅ Enabled               │
│ Priority:          LOWER (catch-all)        │
└─────────────────────────────────────────────┘
```

---

## 📝 Step-by-Step: How to Configure in Dokploy

### Step 1: Access Your Project
1. Log into Dokploy dashboard
2. Go to your `rasa-brizl` project

### Step 2: Configure Webhook Service Domain
1. Find the **`social_media_webhook`** service
2. Click on "Domains" or "Domain Settings"
3. Click "Add Domain"
4. Fill in:
   - **Host:** `selmedia.net`
   - **Path:** `/webhooks`
   - **Container Port:** `5000`
   - **HTTPS:** Enable
   - **Certificate:** Let's Encrypt
   - **Strip Path:** NO (uncheck if available)

### Step 3: Verify Existing Rasa Domain
1. Find the **`rasa`** service
2. Verify existing domain configuration:
   - **Host:** `selmedia.net`
   - **Path:** `/`
   - **Container Port:** `3000`

### Step 4: Set Priority (if available)
- Webhook domain (`/webhooks`) should have **HIGHER priority**
- Rasa domain (`/`) should have **LOWER priority**
- This ensures `/webhooks` is matched before `/`

### Step 5: Save and Deploy
1. Save all changes
2. Wait for deployment (30-60 seconds)
3. Test endpoints

---

## 🧪 Testing After Configuration

### Test 1: Rasa Service (should still work)
```bash
curl https://selmedia.net/
```
**Expected:** `Hello from Rasa: 3.6.0`

### Test 2: Health Endpoint
```bash
curl https://selmedia.net/health
```
**Expected:** JSON response from webhook service
```json
{
  "status": "healthy",
  "service": "social_media_webhook",
  ...
}
```

### Test 3: Facebook Webhook
```bash
curl "https://selmedia.net/webhooks/facebook/webhook?hub.mode=subscribe&hub.verify_token=vera_fb_verify_2024&hub.challenge=test123"
```
**Expected:** `test123`

### Test 4: WhatsApp Webhook
```bash
curl "https://selmedia.net/webhooks/whatsapp/webhook?hub.mode=subscribe&hub.verify_token=vera_wa_verify_2024&hub.challenge=test456"
```
**Expected:** `test456`

---

## 🔍 Alternative: If Dokploy Doesn't Support Path-Based Routing

Some Dokploy versions might not support path-based routing well. If that's the case:

### Option A: Use Port in Domain Configuration
Instead of path-based routing, you might need to configure the webhook service to be accessible on a different port or subdomain.

### Option B: Use Traefik Labels (Advanced)
Add custom Traefik labels to your docker-compose.yml:

```yaml
social_media_webhook:
  # ... existing config ...
  labels:
    - "traefik.enable=true"
    - "traefik.http.routers.webhooks.rule=Host(`selmedia.net`) && PathPrefix(`/webhooks`)"
    - "traefik.http.routers.webhooks.entrypoints=websecure"
    - "traefik.http.routers.webhooks.tls.certresolver=letsencrypt"
    - "traefik.http.services.webhooks.loadbalancer.server.port=5000"
```

### Option C: Use Subdomain
Create a subdomain for webhooks:
1. Add DNS: `webhooks.selmedia.net` (A record to 23.88.104.97)
2. Configure in Dokploy:
   - Host: `webhooks.selmedia.net`
   - Port: `5000`
3. Update Facebook/WhatsApp URLs to:
   - `https://webhooks.selmedia.net/webhooks/facebook/webhook`

---

## 📊 Current Routing Flow

**What happens now:**
```
https://selmedia.net/
    ↓
Dokploy → Port 3000 (Rasa) ✅ Works

https://selmedia.net/webhooks/facebook/webhook
    ↓
Dokploy → Port 3000 (Rasa) ❌ 502 Error
          (Rasa doesn't have /webhooks/facebook/webhook endpoint)
```

**What should happen:**
```
https://selmedia.net/
    ↓
Dokploy → Port 3000 (Rasa) ✅

https://selmedia.net/webhooks/facebook/webhook
    ↓
Dokploy → Port 5000 (social_media_webhook) ✅
```

---

## ✅ Checklist

- [ ] Access Dokploy dashboard
- [ ] Find `social_media_webhook` service
- [ ] Add domain with path `/webhooks` pointing to port 5000
- [ ] Verify `rasa` service has domain `/` pointing to port 3000
- [ ] Set priorities correctly (webhooks higher, rasa lower)
- [ ] Save and deploy
- [ ] Test health endpoint
- [ ] Test Facebook webhook verification
- [ ] Test WhatsApp webhook verification
- [ ] Configure webhooks in Facebook Developer Console

---

## 📞 Next Steps

1. **Configure Dokploy routing** as described above
2. **Test all endpoints** to verify routing works
3. **Configure Facebook/WhatsApp webhooks** with correct URLs
4. **Monitor logs** to ensure messages flow correctly

**You're almost there!** DNS is fixed, services are running - you just need the routing configuration! 🚀
