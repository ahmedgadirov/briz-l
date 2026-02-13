# VERA Platform Detection Guide

## Overview

VERA now includes **intelligent platform detection** that allows the bot to identify which platform a user is messaging from and adapt responses accordingly.

## Supported Platforms

| Platform | Detection Method | Response Style |
|----------|------------------|----------------|
| **WhatsApp** | `whatsapp_` prefix in sender_id | Short, emoji-friendly, no buttons |
| **Facebook Messenger** | `facebook_` prefix in sender_id | Balanced, supports buttons (max 3) |
| **Instagram DM** | `instagram_` prefix in sender_id | Short, visual-friendly, no buttons |
| **Telegram** | `telegram_` prefix in sender_id | Detailed, supports formatting |
| **Website Chat** | `web-` prefix in sender_id | Professional, full features |

## How It Works

### 1. Platform Detection

The system detects the platform from:

1. **Metadata** (most reliable) - passed explicitly in the message
2. **Sender ID prefix** - fallback detection from user ID format

```python
# Example sender IDs:
# WhatsApp: whatsapp_994555512400
# Facebook: facebook_123456789
# Instagram: instagram_987654321
# Telegram: telegram_555123456
# Website: web-1707891234567-abc123
```

### 2. Platform-Specific Adaptations

Each platform has unique characteristics that VERA adapts to:

#### WhatsApp 📱
- **Max message length**: 1000 characters
- **Buttons**: NOT supported → Uses numbered lists instead
- **Emoji**: ✅ Friendly
- **Tone**: Casual and conversational
- **CTA**: "WhatsApp üzərindən əlaqə"

#### Facebook Messenger 💬
- **Max message length**: 2000 characters
- **Buttons**: ✅ Up to 3 buttons
- **Emoji**: ✅ Friendly
- **Tone**: Balanced
- **CTA**: "Messenger ilə yaz"

#### Instagram DM 📸
- **Max message length**: 1000 characters
- **Buttons**: NOT supported → Plain text only
- **Emoji**: ✅ Very friendly
- **Tone**: Visual and trendy
- **CTA**: "DM göndər"

#### Telegram 📨
- **Max message length**: 4000 characters
- **Buttons**: ✅ Supported
- **Formatting**: Bold, italic, links
- **Tone**: Professional
- **CTA**: "Telegram bot"

#### Website Chat 💻
- **Max message length**: 2000 characters
- **Buttons**: ✅ Supported
- **Features**: Full functionality
- **Tone**: Professional
- **CTA**: "Müayinəyə yazıl"

## Implementation Details

### Backend (Python)

#### User Profiler (`intelligence/user_profiler.py`)

```python
from intelligence.user_profiler import UserProfiler

profiler = UserProfiler()

# Analyze user with platform detection
profile = profiler.analyze_user(
    user_id="whatsapp_994555512400",
    message="Gözüm ağrıyır",
    conversation_history=[],
    metadata={"platform": "whatsapp"}  # Optional, auto-detected from ID
)

print(profile['platform'])  # 'whatsapp'
print(profile['supports_buttons'])  # False
print(profile['preferred_response_style'])  # 'concise'
```

#### Response Generator (`actions/response_generator.py`)

The action automatically:
1. Detects platform from metadata or sender_id
2. Generates platform-adaptive prompts
3. Logs platform information for debugging

```python
# In the action logs:
📱 PLATFORM DETECTED: whatsapp (user_id: whatsapp_994555512400)
🧠 USER PROFILE: {'platform': 'whatsapp', 'supports_buttons': False, ...}
```

### Frontend (TypeScript/React)

#### API Client (`brizl-clinic/lib/rasa-api.ts`)

```typescript
import { sendMessageToRasa } from '@/lib/rasa-api'

// Send message with platform metadata
const responses = await sendMessageToRasa(sessionId, message, {
  platform: 'web',
  source: 'website_chat',
  is_button_click: false,
})
```

#### Chat Hook (`brizl-clinic/hooks/useChat.tsx`)

```typescript
const { sendMessage } = useChat()

// Automatically includes web platform metadata
await sendMessage('Salam!')
```

### Social Media Webhook (`social_media_webhook.py`)

The webhook automatically adds platform metadata:

```python
# Facebook/Instagram
forward_to_rasa(sender_id, text, platform="facebook")
forward_to_rasa(sender_id, text, platform="instagram")

# WhatsApp
forward_to_rasa(from_phone, text, platform="whatsapp")
```

## Platform Characteristics Reference

```python
PLATFORM_CHARACTERISTICS = {
    'whatsapp': {
        'max_message_length': 1000,
        'supports_buttons': False,
        'supports_lists': True,
        'emoji_friendly': True,
        'informal_tone': True,
        'response_style': 'concise',
        'preferred_cta': 'WhatsApp üzərindən əlaqə'
    },
    'facebook': {
        'max_message_length': 2000,
        'supports_buttons': True,
        'supports_lists': False,
        'emoji_friendly': True,
        'informal_tone': True,
        'response_style': 'balanced',
        'preferred_cta': 'Messenger ilə yaz'
    },
    'instagram': {
        'max_message_length': 1000,
        'supports_buttons': False,
        'supports_lists': False,
        'emoji_friendly': True,
        'informal_tone': True,
        'response_style': 'visual_friendly',
        'preferred_cta': 'DM göndər'
    },
    'telegram': {
        'max_message_length': 4000,
        'supports_buttons': True,
        'supports_lists': True,
        'emoji_friendly': True,
        'informal_tone': False,
        'response_style': 'detailed',
        'preferred_cta': 'Telegram bot'
    },
    'web': {
        'max_message_length': 2000,
        'supports_buttons': True,
        'supports_lists': True,
        'emoji_friendly': True,
        'informal_tone': False,
        'response_style': 'professional',
        'preferred_cta': 'Müayinəyə yazıl'
    }
}
```

## Adaptive Prompts

VERA generates platform-specific prompts that guide the LLM:

### Example: WhatsApp Prompt
```
**PLATFORM: WhatsApp 📱**
- QISA və MOBIL-dostu cavablar yaz (maksimum 1000 xarakter)
- Emoji istifadə et ✅ 👁️ 🏥
- Düymələr YOXDUR - əvəzinə nömrələnmiş siyahı yaz (1️⃣ 2️⃣ 3️⃣)
- Sərbəst, rahat dil istifadə et
- WhatsApp linkləri ver: wa.me/994555512400
```

### Example: Website Prompt
```
**PLATFORM: Website Chat 💻**
- Profesional və ətraflı cavablar
- Düymələr mövcuddur
- Strukturlaşdırılmış məlumat ver
- Website üçün optimizasiya et
- Call-to-action düymələri tövsiyə et
```

## Testing Platform Detection

### Test via API

```bash
# Test WhatsApp
curl -X POST http://localhost:5005/webhooks/rest/webhook \
  -H "Content-Type: application/json" \
  -d '{
    "sender": "whatsapp_994555512400",
    "message": "Salam",
    "metadata": {"platform": "whatsapp"}
  }'

# Test Website
curl -X POST http://localhost:5005/webhooks/rest/webhook \
  -H "Content-Type: application/json" \
  -d '{
    "sender": "web-test-123",
    "message": "Salam",
    "metadata": {"platform": "web"}
  }'
```

### Check Logs

Look for these log messages:
```
📱 PLATFORM DETECTED: whatsapp (user_id: whatsapp_994555512400)
📱 Platform metadata: {'platform': 'whatsapp', 'supports_buttons': False, ...}
```

## Benefits

1. **Better User Experience**: Messages are optimized for each platform
2. **Higher Engagement**: Platform-appropriate CTAs and formatting
3. **Consistent Branding**: VERA adapts while maintaining professionalism
4. **Analytics Ready**: Track performance by platform
5. **Future-Proof**: Easy to add new platforms

## Adding New Platforms

To add a new platform:

1. Add to `PLATFORM_PATTERNS` in `user_profiler.py`:
```python
'new_platform': {
    'prefixes': ['newplatform_', 'np_'],
    'keywords': ['new platform'],
    'characteristics': []
}
```

2. Add to `PLATFORM_CHARACTERISTICS`:
```python
'new_platform': {
    'max_message_length': 2000,
    'supports_buttons': True,
    'supports_lists': True,
    'emoji_friendly': True,
    'informal_tone': False,
    'response_style': 'balanced',
    'preferred_cta': 'Action button'
}
```

3. Add platform prompt in `generate_adaptive_prompt()`

4. Update webhook handler if needed

---

**Created**: February 2026  
**Version**: 1.0  
**Author**: VERA Development Team