"""
Admin Handler - Vera for Seljan
Provides unlimited AI assistant capabilities for the admin user
"""

import os
from typing import Dict, Any, Optional
import requests
from marketing.analytics import MarketingAnalytics

# Seljan's WhatsApp number
ADMIN_NUMBER = "994502115120"

def is_admin(phone_number: str) -> bool:
    """Check if the phone number belongs to Seljan (admin)"""
    # Remove any country code variations
    clean_number = phone_number.replace("+", "").replace(" ", "")
    return clean_number == ADMIN_NUMBER


def generate_admin_system_prompt() -> str:
    """
    Generate system prompt for Vera when talking to Seljan
    Different from regular medical assistant prompt
    """
    return """You are Vera, Seljan's personal AI assistant for Briz-L Aesthetic Clinic.

Your primary role is to help Seljan manage and understand her clinic's performance, but you can also help with ANY task she needs.

When Seljan messages you:
1. Start with clinic updates if relevant (new leads, hot prospects, conversions)
2. Be warm, supportive, and professional
3. You have UNLIMITED AI access - no restrictions on what you can help with
4. You can write articles, create content, answer questions, analyze data, or anything else

Personality:
- Warm and supportive
- Professional but friendly
- Proactive with clinic insights
- Always ready to help with any task

Address her as "Seljan" when appropriate.

If she asks for clinic reports, provide clear, actionable insights.
If she asks for other tasks (writing, research, etc.), help without limits!"""


def get_quick_clinic_update() -> str:
    """Get quick clinic stats for Seljan"""
    try:
        analytics = MarketingAnalytics()
        stats = analytics.get_lead_stats()
        
        return f"""📊 Quick Update:
• Total Leads: {stats['total_leads']}
• Hot Leads: {stats['hot_leads']}
• New Today: {stats['today_leads']}"""
    except Exception as e:
        return "📊 (Analytics temporarily unavailable)"


def generate_admin_greeting() -> str:
    """Generate personalized greeting for Seljan"""
    clinic_update = get_quick_clinic_update()
    
    return f"""Hello Seljan! 👋 Vera here.

{clinic_update}

How can I help you today? I'm ready to assist with clinic reports, writing, or anything else you need! ✨"""


def handle_admin_message(message: str, include_stats: bool = True) -> Dict[str, Any]:
    """
    Process admin message with special handling
    
    Args:
        message: Message from Seljan
        include_stats: Whether to include clinic stats in context
        
    Returns:
        Dict with system_prompt and additional context
    """
    system_prompt = generate_admin_system_prompt()
    
    # Add clinic context if requested
    context = ""
    if include_stats:
        try:
            analytics = MarketingAnalytics()
            stats = analytics.get_lead_stats()
            context = f"\n\nCurrent clinic stats: {stats['total_leads']} total leads, {stats['hot_leads']} hot leads, {stats['today_leads']} new today."
        except:
            pass
    
    return {
        "system_prompt": system_prompt,
        "context": context,
        "unlimited": True,  # Flag for unlimited AI access
        "is_admin": True
    }


def format_daily_report() -> str:
    """
    Generate formatted daily report for Seljan
    Sent automatically at 9 AM
    """
    try:
        analytics = MarketingAnalytics()
        
        # Get all necessary data
        today = analytics.get_daily_stats()
        week = analytics.get_weekly_stats()
        funnel = analytics.get_conversion_funnel()
        top_surgeries = analytics.get_top_surgeries(3)
        recent_hot = analytics.get_recent_hot_leads(3)
        
        # Build report
        report = f"""🌅 Good morning Seljan!

📊 **Your Briz-L Update for {today.get('date', 'today')}**

**Yesterday's Performance:**
• New Leads: {today.get('total_leads', 0)}
• Hot Leads: {today.get('hot_leads', 0)}
• Booking Intents: {today.get('booking_intents', 0)}
• Follow-ups Sent: {today.get('follow_ups_sent', 0)}

**This Week So Far:**
• Total Leads: {week.get('total_leads', 0)}
• Hot Leads: {week.get('hot_leads', 0)}
• Booking Intents: {week.get('booking_intents', 0)}
"""
        
        # Add conversion funnel
        funnel_data = funnel.get('funnel', {})
        rates = funnel.get('rates', {})
        if funnel_data:
            report += f"""
📈 **Conversion Funnel:**
• Total Leads: {funnel_data.get('total_leads', 0)}
• Hot Leads: {funnel_data.get('hot_leads', 0)} ({rates.get('hot_lead_rate', 0)}%)
• Booking Intents: {funnel_data.get('booking_intents', 0)} ({rates.get('intent_rate', 0)}%)
• Converted: {funnel_data.get('converted', 0)} ({rates.get('conversion_rate', 0)}%)
"""
        
        # Add top surgeries
        if top_surgeries:
            report += "\n🏥 **Top Inquiries:**\n"
            for i, surgery in enumerate(top_surgeries, 1):
                report += f"{i}. {surgery['surgery']} ({surgery['inquiry_count']})\n"
        
        # Add hot leads to follow up
        if recent_hot:
            report += "\n🔥 **Hot Leads to Follow Up:**\n"
            for lead in recent_hot:
                user_id = lead['user_id']
                score = lead['lead_score']
                surgeries = ", ".join(lead.get('surgeries_interested', [])[:2]) if lead.get('surgeries_interested') else "General"
                report += f"• {user_id[:15]}... - {surgeries} (Score: {score})\n"
        
        report += """
💡 **What would you like me to help with today?**
I'm here for reports, analysis, or anything else!

- Vera 💪"""
        
        return report
        
    except Exception as e:
        return f"""Good morning Seljan! ☀️

I encountered an issue generating your full report, but I'm here and ready to help with anything you need!

Error: {str(e)}

- Vera"""


def send_whatsapp_to_admin(message: str) -> bool:
    """
    Send WhatsApp message to Seljan
    
    Args:
        message: Message text to send
        
    Returns:
        True if successful, False otherwise
    """
    try:
        wa_access_token = os.getenv("WA_ACCESS_TOKEN")
        wa_phone_number_id = os.getenv("WA_PHONE_NUMBER_ID")
        
        if not wa_access_token or not wa_phone_number_id:
            print("❌ WhatsApp credentials not configured")
            return False
        
        url = f"https://graph.facebook.com/v18.0/{wa_phone_number_id}/messages"
        
        headers = {
            "Authorization": f"Bearer {wa_access_token}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": ADMIN_NUMBER,
            "type": "text",
            "text": {
                "preview_url": False,
                "body": message
            }
        }
        
        response = requests.post(url, json=payload, headers=headers, timeout=10)
        response.raise_for_status()
        
        print(f"✅ Message sent to Seljan successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Error sending message to Seljan: {e}")
        return False


if __name__ == "__main__":
    # Test the admin handler
    print("Testing Admin Handler...")
    print("\n" + "="*60)
    print(is_admin("994502115120"))
    print(is_admin("+994502115120"))
    print(is_admin("994502118516"))  # Should be False
    print("="*60 + "\n")
    
    print("Generating daily report...")
    print("\n" + "="*60)
    print(format_daily_report())
    print("="*60 + "\n")
