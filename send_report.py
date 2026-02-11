#!/usr/bin/env python3
"""
Send Report to Seljan - CLI Tool
Usage: python send_report.py [--type daily|weekly|monthly|custom]
"""

import sys
import argparse
from admin_handler import send_whatsapp_to_admin, format_daily_report
from marketing.analytics import MarketingAnalytics


def format_weekly_report() -> str:
    """Generate weekly report"""
    try:
        analytics = MarketingAnalytics()
        week = analytics.get_weekly_stats()
        funnel = analytics.get_conversion_funnel()
        top_surgeries = analytics.get_top_surgeries(5)
        engagement = analytics.get_engagement_metrics()
        
        report = f"""📅 **Weekly Report for Seljan**

**This Week's Performance:**
• Total Leads: {week.get('total_leads', 0)}
• Hot Leads: {week.get('hot_leads', 0)}
• Booking Intents: {week.get('booking_intents', 0)}
• Follow-ups Sent: {week.get('follow_ups_sent', 0)}
• Responses: {week.get('follow_up_responses', 0)}

📊 **Engagement Metrics:**
• Avg Messages/Lead: {engagement.get('avg_messages_per_lead', 0)}
• Avg Lead Score: {engagement.get('avg_lead_score', 0)}
• Highly Engaged: {engagement.get('highly_engaged_leads', 0)}

📈 **Conversion Funnel:**
"""
        funnel_data = funnel.get('funnel', {})
        rates = funnel.get('rates', {})
        report += f"""• Total: {funnel_data.get('total_leads', 0)}
• Hot: {funnel_data.get('hot_leads', 0)} ({rates.get('hot_lead_rate', 0)}%)
• Intent: {funnel_data.get('booking_intents', 0)} ({rates.get('intent_rate', 0)}%)
• Converted: {funnel_data.get('converted', 0)} ({rates.get('conversion_rate', 0)}%)

🏥 **Top Surgeries This Week:**
"""
        for i, surgery in enumerate(top_surgeries, 1):
            report += f"{i}. {surgery['surgery']} ({surgery['inquiry_count']})\n"
        
        report += "\n- Vera 💪"
        return report
        
    except Exception as e:
        return f"Error generating weekly report: {str(e)}"


def format_monthly_report() -> str:
    """Generate monthly report"""
    try:
        analytics = MarketingAnalytics()
        month = analytics.get_monthly_stats()
        funnel = analytics.get_conversion_funnel()
        top_surgeries = analytics.get_top_surgeries(10)
        distribution = analytics.get_lead_distribution()
        
        report = f"""📆 **Monthly Report for Seljan**

**This Month's Performance:**
• Total Leads: {month.get('total_leads', 0)}
• Hot Leads: {month.get('hot_leads', 0)}
• Booking Intents: {month.get('booking_intents', 0)}
• Follow-ups Sent: {month.get('follow_ups_sent', 0)}

📊 **Lead Distribution:**
"""
        for status, data in distribution.items():
            report += f"• {status.upper()}: {data['count']} ({data['percentage']}%)\n"
        
        report += "\n📈 **Conversion Rates:**\n"
        rates = funnel.get('rates', {})
        report += f"""• Engagement: {rates.get('engagement_rate', 0)}%
• Hot Lead: {rates.get('hot_lead_rate', 0)}%
• Intent: {rates.get('intent_rate', 0)}%
• Conversion: {rates.get('conversion_rate', 0)}%

🏥 **Top 10 Surgeries:**
"""
        for i, surgery in enumerate(top_surgeries, 1):
            report += f"{i}. {surgery['surgery']} ({surgery['inquiry_count']})\n"
        
        report += "\n- Vera 💪"
        return report
        
    except Exception as e:
        return f"Error generating monthly report: {str(e)}"


def main():
    parser = argparse.ArgumentParser(
        description='Send reports to Seljan via WhatsApp'
    )
    parser.add_argument(
        '--type',
        choices=['daily', 'weekly', 'monthly', 'custom'],
        default='daily',
        help='Type of report to send (default: daily)'
    )
    parser.add_argument(
        '--message',
        type=str,
        help='Custom message to send (used with --type custom)'
    )
    
    args = parser.parse_args()
    
    # Generate report based on type
    if args.type == 'daily':
        print("📊 Generating daily report...")
        message = format_daily_report()
    elif args.type == 'weekly':
        print("📅 Generating weekly report...")
        message = format_weekly_report()
    elif args.type == 'monthly':
        print("📆 Generating monthly report...")
        message = format_monthly_report()
    elif args.type == 'custom':
        if not args.message:
            print("❌ Error: --message required for custom type")
            sys.exit(1)
        message = args.message
    
    # Send to Seljan
    print(f"\n📱 Sending to Seljan...")
    print("-" * 60)
    print(message)
    print("-" * 60)
    
    success = send_whatsapp_to_admin(message)
    
    if success:
        print("\n✅ Report sent successfully to Seljan!")
    else:
        print("\n❌ Failed to send report. Check logs for details.")
        sys.exit(1)


if __name__ == "__main__":
    main()
