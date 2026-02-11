# 🤖 VERA Bot Naming System

## Overview
The Briz-L Eye Clinic chatbot uses a dual-naming system:
- **VERA** - Virtual Eye-care Representative Assistant (Customer-facing)
- **VERA MAX** - Admin version (Future implementation)

---

## Current Implementation: VERA (Customer Version)

### Identity
- **Name**: VERA
- **Full Name**: Virtual Eye-care Representative Assistant
- **Purpose**: Customer service, medical guidance, appointment scheduling
- **Personality**: Empathetic, professional, intelligent medical assistant

### Configuration Files

#### 1. actions/response_generator.py
```python
SYSTEM_PROMPT = """
Adın: VERA (Virtual Eye-care Representative Assistant)
Məqsəd: Briz-L Göz Klinikasının müştərilərinə professional və empatik xidmət
"""
```

#### 2. domain.yml
```yaml
responses:
  utter_greet:
    - text: "Salam! Mən VERA, Briz-L Göz Klinikasının virtual köməkçisiyəm. 👋"
```

#### 3. config.yml
```yaml
assistant_id: vera-customer-assistant
```

---

## Future Implementation: VERA MAX (Admin Version)

### Planned Features
VERA MAX will be an enhanced version for **administrative staff** with additional capabilities:

#### Core Differences from VERA
| Feature | VERA (Customer) | VERA MAX (Admin) |
|---------|----------------|------------------|
| **User Access** | Public customers | Internal admin staff |
| **Capabilities** | Info, triage, booking assistance | Analytics, lead management, reporting |
| **Data Access** | Limited to public info | Full database access |
| **Actions** | View-only, recommend | Create, update, delete records |

#### Suggested Admin Features
1. **Marketing Analytics**
   - View lead scores and conversion rates
   - Analyze customer engagement patterns
   - Generate marketing reports

2. **Database Management**
   - View and update customer records
   - Manage appointment schedules
   - Track follow-up communications

3. **System Monitoring**
   - Bot performance metrics
   - Message volume analysis
   - Error tracking and debugging

4. **Advanced Actions**
   - Manual lead scoring adjustments
   - Custom message broadcasting
   - A/B testing for responses

### Implementation Approach

#### Option 1: Role-Based Access (Recommended)
Add role detection to the bot based on user ID or admin token:

```python
# In actions/response_generator.py
def get_user_role(user_id):
    """Determine if user is customer or admin"""
    admin_ids = os.getenv("ADMIN_USER_IDS", "").split(",")
    return "admin" if str(user_id) in admin_ids else "customer"

# Modify SYSTEM_PROMPT dynamically
if user_role == "admin":
    system_prompt = VERA_MAX_SYSTEM_PROMPT
else:
    system_prompt = SYSTEM_PROMPT
```

#### Option 2: Separate Bot Instance
Create a second Rasa instance for admin:
- Separate Telegram bot token
- Different endpoint configuration
- Admin-only commands and features

#### Option 3: Command-Based Mode Switching
Allow admin users to switch modes with commands:
```
/admin - Switch to VERA MAX mode
/customer - Switch back to VERA mode
```

### Environment Variables for VERA MAX
```bash
# .env additions
ADMIN_USER_IDS=123456789,987654321  # Telegram admin user IDs
VERA_MODE=customer  # or 'admin' for VERA MAX
ADMIN_SECRET_KEY=your-secret-key
```

### VERA MAX System Prompt Template
```python
VERA_MAX_SYSTEM_PROMPT = """
Sən "Briz-L Göz Klinikası"nın ADMİN KÖMƏKÇI sistemisən.
Adın: VERA MAX (Virtual Eye-care Representative Assistant - MAX Edition)
Məqsəd: Klinika administratorlarına analitik və idarəetmə dəstəyi

**ƏSAS YETKİLƏR:**
- Marketing və lead analitikası
- Müştəri databazası sorğuları
- Performans metrikləri
- Follow-up planlaması
- Sistem konfiqurasiyası

**CAVAB FORMATI:**
- Texniki və dəqiq məlumat ver
- Statistik məlumatlar göstər
- Təhlil və tövsiyələr təqdim et
- Admin səviyyəli terminologiya istifadə et
"""
```

---

## Implementation Checklist for VERA MAX

When you're ready to implement VERA MAX, follow these steps:

- [ ] Determine access control method (role-based, separate instance, or command-based)
- [ ] Create VERA_MAX_SYSTEM_PROMPT in response_generator.py
- [ ] Add admin user ID detection logic
- [ ] Create admin-specific intents and responses in domain.yml
- [ ] Implement admin-only actions:
  - [ ] action_view_analytics
  - [ ] action_search_leads
  - [ ] action_generate_report
  - [ ] action_update_lead_status
- [ ] Add environment variables for admin configuration
- [ ] Create admin dashboard interface (optional)
- [ ] Update documentation with admin commands
- [ ] Test admin features thoroughly
- [ ] Train model with admin intents

---

## Testing the Current VERA Implementation

### Test Greeting
Send message: `/start` or `Salam`

**Expected Response:**
```
Salam! Mən VERA, Briz-L Göz Klinikasının virtual köməkçisiyəm. 👋 
Sizə necə kömək edə bilərəm?
```

### Verify Bot Identity
The bot should:
- Introduce itself as "VERA"
- Mention it's the virtual assistant for Briz-L
- Maintain professional, empathetic tone
- Use Azerbaijani language

---

## Branding Guidelines

### VERA (Customer)
✅ **Use these phrases:**
- "Mən VERA"
- "VERA kimi"
- "Virtual köməkçiniz"
- "Briz-L Göz Klinikasının assistenti"

❌ **Avoid:**
- "Bot"
- "AI system"
- Technical jargon
- Overly formal titles

### VERA MAX (Admin) - Future
✅ **Use these phrases:**
- "VERA MAX - Admin Edition"
- "Administrator paneli"
- "Enhanced analytics"
- Technical terminology is acceptable

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2026-02-11 | Initial VERA implementation (customer version) |
| 2.0 | TBD | VERA MAX implementation planned |

---

## Notes
- Current implementation: **VERA (Customer version only)**
- VERA MAX is prepared for future implementation
- All admin features should be behind authentication
- Maintain separation between customer and admin data access

**For questions or implementation assistance, refer to this guide.**
