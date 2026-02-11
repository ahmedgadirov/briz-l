#!/usr/bin/env python3
"""
Daily Report Scheduler - Sends automated reports to Seljan at 9:00 AM
"""

import schedule
import time
import logging
from datetime import datetime
from admin_handler import format_daily_report, send_whatsapp_to_admin

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def send_daily_report():
    """Send the daily report to Seljan"""
    try:
        logger.info("⏰ Time to send daily report to Seljan...")
        
        # Generate report
        report = format_daily_report()
        
        # Send to Seljan
        success = send_whatsapp_to_admin(report)
        
        if success:
            logger.info("✅ Daily report sent successfully to Seljan!")
        else:
            logger.error("❌ Failed to send daily report")
            
    except Exception as e:
        logger.error(f"❌ Error sending daily report: {e}")


def main():
    """Main scheduler loop"""
    logger.info("🚀 Starting Daily Report Scheduler for Seljan")
    logger.info("📅 Reports will be sent at 9:00 AM daily")
    
    # Schedule daily report at 9:00 AM
    schedule.every().day.at("09:00").do(send_daily_report)
    
    # Also schedule a test report 1 minute from now (for testing)
    # Uncomment this line to test immediately:
    # schedule.every(1).minutes.do(send_daily_report)
    
    logger.info("✅ Scheduler is running...")
    logger.info(f"⏰ Next report scheduled for: {schedule.next_run()}")
    
    # Keep the scheduler running
    try:
        while True:
            schedule.run_pending()
            time.sleep(60)  # Check every minute
            
    except KeyboardInterrupt:
        logger.info("\n👋 Scheduler stopped by user")
    except Exception as e:
        logger.error(f"❌ Scheduler error: {e}")


if __name__ == "__main__":
    main()
