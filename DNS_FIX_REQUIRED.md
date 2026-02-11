# 🔧 DNS FIX REQUIRED

## ⚠️ Problem Identified

Your domain `selmedia.net` is pointing to the **WRONG IP ADDRESS**:

```
❌ Current DNS:  216.24.57.1  (Wrong server - suspended)
✅ Should be:    23.88.104.97  (Your actual Dokploy server)
```

---

## 🚀 Quick Fix - Update Cloudflare DNS

### Step-by-Step Instructions:

**1. Go to Cloudflare Dashboard:**
   - Login at https://dash.cloudflare.com
   - Select your domain: `selmedia.net`

**2. Click on "DNS" in the left menu**

**3. Find the A Record for your root domain:**
   ```
   Type: A
   Name: @ (or selmedia.net)
   Content: 216.24.57.1  ← THIS IS WRONG!
   ```

**4. Click "Edit" on that record**

**5. Change the IP address:**
   ```
   FROM: 216.24.57.1
   TO:   23.88.104.97
   ```

**6. Make sure Proxy Status is set:**
   - Either: Orange cloud (Proxied) - for DDoS protection and CDN
   - Or: Gray cloud (DNS only) - direct to your server

**7. Click "Save"**

**8. Wait 1-2 minutes for DNS propagation**

---

## ✅ Verify the Fix

After updating DNS, test with these commands:

### 1. Check DNS Resolution:
```bash
nslookup selmedia.net
# Should show: 23.88.104.97 (or Cloudflare IP if proxied)
```

### 2. Test Health Endpoint:
```bash
curl https://selmedia.net/health
```

**Expected response:**
```json
{
  "status": "healthy",
  "service": "social_media_webhook",
  ...
}
```

### 3. Test Facebook Webhook:
```bash
curl "https://selmedia.net/webhooks/facebook/webhook?hub.mode=subscribe&hub.verify_token=vera_fb_verify_2024&hub.challenge=test123"
```

**Expected response:**
```
test123
```

### 4. Test WhatsApp Webhook:
```bash
curl "https://selmedia.net/webhooks/whatsapp/webhook?hub.mode=subscribe&hub.verify_token=vera_wa_verify_2024&hub.challenge=test456"
```

**Expected response:**
```
test456
```

---

## 📱 After DNS is Fixed

Once the DNS points to the correct IP (`23.88.104.97`), configure your webhooks:

### Facebook & Instagram:
```
Callback URL: https://selmedia.net/webhooks/facebook/webhook
Verify Token: vera_fb_verify_2024
Subscribe to: messages, messaging_postbacks
```

### WhatsApp:
```
Callback URL: https://selmedia.net/webhooks/whatsapp/webhook
Verify Token: vera_wa_verify_2024
Subscribe to: messages
```

---

## 🔍 DNS Propagation

After updating DNS:
- **Immediate:** Your computer might still cache old DNS (1-2 minutes)
- **Cloudflare:** Updates instantly in their network
- **Global DNS:** Can take up to 24 hours (usually 5-10 minutes)

To flush your local DNS cache:
```bash
# macOS
sudo dscacheutil -flushcache; sudo killall -HUP mDNSResponder

# Check current resolution
dig selmedia.net +short
```

---

## 📊 Summary

**What went wrong:**
- Your DNS was pointing to old/wrong server IP (216.24.57.1)
- That server is suspended or doesn't exist
- Your actual Dokploy server is at 23.88.104.97

**What to do:**
1. Login to Cloudflare
2. Update A record from 216.24.57.1 → 23.88.104.97
3. Save changes
4. Wait 1-2 minutes
5. Test webhooks

**Your Dokploy works perfectly!** ✅  
**You just need to update DNS to point to the right server!** 🎯
