#!/usr/bin/env python3
"""
Marketing Dashboard Viewer
Quick view of marketing performance
"""

import sys
import os

sys.path.insert(0, os.path.dirname(__file__))

from marketing.analytics import MarketingAnalytics
from marketing.lead_tracker import LeadTracker
from marketing.follow_up_scheduler import FollowUpScheduler


def main():
    """Display marketing dashboard"""
    
    try:
        # Display main dashboard
        analytics = MarketingAnalytics()
        analytics.print_dashboard()
        
        # Additional insights
        tracker = LeadTracker()
        scheduler = FollowUpScheduler()
        
        print("🔥 HOT LEADS (Top 5):")
        hot_leads = tracker.get_hot_leads(limit=5)
        for lead in hot_leads:
            print(f"  • User: {lead['user_id'][:10]}... | "
                  f"Score: {lead['lead_score']} | "
                  f"Surgeries: {', '.join(lead.get('surgeries_interested', [])[:2])}")
        
        print()
        print("📧 FOLLOW-UP EFFECTIVENESS:")
        effectiveness = scheduler.get_follow_up_effectiveness()
        print(f"  • Total Sent: {effectiveness.get('total_sent', 0)}")
        print(f"  • Responses: {effectiveness.get('total_responses', 0)}")
        print(f"  • Response Rate: {effectiveness.get('overall_response_rate', 0)}%")
        
        print()
        print("💡 ENGAGEMENT METRICS:")
        engagement = analytics.get_engagement_metrics()
        print(f"  • Avg Messages/Lead: {engagement.get('avg_messages_per_lead', 0)}")
        print(f"  • Avg Lead Score: {engagement.get('avg_lead_score', 0)}")
        print(f"  • Highly Engaged: {engagement.get('highly_engaged_leads', 0)}")
        
        print("\n" + "="*60 + "\n")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        print("\nMake sure database is initialized:")
        print("  python3 init_marketing_db.py")


if __name__ == "__main__":
    main()
