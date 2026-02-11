#!/usr/bin/env python3
"""
Database Initialization Script for Briz-L Marketing System
Run this script to create all marketing database tables
"""

import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(__file__))

from marketing.database import init_marketing_database
from marketing.analytics import MarketingAnalytics


def main():
    """Initialize marketing database and run basic checks"""
    print("=" * 60)
    print("🚀 BRIZ-L MARKETING DATABASE INITIALIZATION")
    print("=" * 60)
    print()
    
    try:
        # Initialize database tables
        print("📊 Creating database tables...")
        init_marketing_database()
        print()
        
        # Test analytics connection
        print("🔍 Testing analytics system...")
        analytics = MarketingAnalytics()
        stats = analytics.get_lead_stats()
        
        print(f"✅ Database initialized successfully!")
        print(f"   • Total leads: {stats.get('total_leads', 0)}")
        print(f"   • Hot leads: {stats.get('hot_leads', 0)}")
        print(f"   • Today's leads: {stats.get('today_leads', 0)}")
        print()
        
        print("=" * 60)
        print("✅ MARKETING SYSTEM READY!")
        print("=" * 60)
        print()
        print("Next steps:")
        print("1. Start your Rasa bot")
        print("2. Leads will be automatically tracked")
        print("3. Use marketing/analytics.py to view performance")
        print()
        
        return True
        
    except Exception as e:
        print(f"❌ ERROR: {e}")
        print()
        print("Troubleshooting:")
        print("1. Check database credentials in .env file")
        print("2. Ensure PostgreSQL is running")
        print("3. Verify network connectivity to database")
        print()
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
