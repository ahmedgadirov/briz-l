"""
Marketing Analytics - Track and analyze marketing performance
"""

from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from .database import db


class MarketingAnalytics:
    """Provides analytics and insights on marketing performance"""
    
    def __init__(self):
        self.db = db
    
    def get_daily_stats(self, date: Optional[str] = None) -> Dict[str, Any]:
        """
        Get marketing stats for a specific date
        
        Args:
            date: Date string (YYYY-MM-DD) or None for today
        
        Returns:
            Dict with daily statistics
        """
        date_param = date if date else 'CURRENT_DATE'
        
        query = f"""
            SELECT * FROM marketing_analytics
            WHERE date = {date_param};
        """
        
        try:
            result = self.db.execute_query(query)
            return dict(result[0]) if result else {
                'date': date or datetime.now().date(),
                'total_leads': 0,
                'hot_leads': 0,
                'booking_intents': 0,
                'follow_ups_sent': 0,
                'follow_up_responses': 0
            }
        except Exception as e:
            print(f"❌ Error getting daily stats: {e}")
            return {}
    
    def get_weekly_stats(self) -> Dict[str, Any]:
        """Get last 7 days statistics"""
        query = """
            SELECT 
                SUM(total_leads) as total_leads,
                SUM(hot_leads) as hot_leads,
                SUM(booking_intents) as booking_intents,
                SUM(follow_ups_sent) as follow_ups_sent,
                SUM(follow_up_responses) as follow_up_responses
            FROM marketing_analytics
            WHERE date >= CURRENT_DATE - INTERVAL '7 days';
        """
        
        try:
            result = self.db.execute_query(query)
            return dict(result[0]) if result else {}
        except Exception as e:
            print(f"❌ Error getting weekly stats: {e}")
            return {}
    
    def get_monthly_stats(self) -> Dict[str, Any]:
        """Get current month statistics"""
        query = """
            SELECT 
                SUM(total_leads) as total_leads,
                SUM(hot_leads) as hot_leads,
                SUM(booking_intents) as booking_intents,
                SUM(follow_ups_sent) as follow_ups_sent,
                SUM(follow_up_responses) as follow_up_responses
            FROM marketing_analytics
            WHERE date >= DATE_TRUNC('month', CURRENT_DATE);
        """
        
        try:
            result = self.db.execute_query(query)
            return dict(result[0]) if result else {}
        except Exception as e:
            print(f"❌ Error getting monthly stats: {e}")
            return {}
    
    def get_conversion_funnel(self) -> Dict[str, Any]:
        """
        Get conversion funnel statistics
        
        Returns:
            Dict with funnel metrics
        """
        try:
            # Total leads
            result = self.db.execute_query("""
                SELECT COUNT(*) as count FROM marketing_leads;
            """)
            total_leads = result[0]['count'] if result else 0
            
            # Engaged leads (3+ messages)
            result = self.db.execute_query("""
                SELECT COUNT(*) as count FROM marketing_leads 
                WHERE total_messages >= 3;
            """)
            engaged_leads = result[0]['count'] if result else 0
            
            # Hot leads
            result = self.db.execute_query("""
                SELECT COUNT(*) as count FROM marketing_leads 
                WHERE lead_status = 'hot';
            """)
            hot_leads = result[0]['count'] if result else 0
            
            # Booking intent
            result = self.db.execute_query("""
                SELECT COUNT(*) as count FROM marketing_leads 
                WHERE booking_intent_detected = TRUE;
            """)
            booking_intents = result[0]['count'] if result else 0
            
            # Converted
            result = self.db.execute_query("""
                SELECT COUNT(*) as count FROM marketing_leads 
                WHERE lead_status = 'converted';
            """)
            converted = result[0]['count'] if result else 0
            
            # Calculate conversion rates
            engaged_rate = round(100 * engaged_leads / total_leads, 2) if total_leads > 0 else 0
            hot_rate = round(100 * hot_leads / total_leads, 2) if total_leads > 0 else 0
            intent_rate = round(100 * booking_intents / total_leads, 2) if total_leads > 0 else 0
            conversion_rate = round(100 * converted / total_leads, 2) if total_leads > 0 else 0
            
            return {
                'funnel': {
                    'total_leads': total_leads,
                    'engaged_leads': engaged_leads,
                    'hot_leads': hot_leads,
                    'booking_intents': booking_intents,
                    'converted': converted
                },
                'rates': {
                    'engagement_rate': engaged_rate,
                    'hot_lead_rate': hot_rate,
                    'intent_rate': intent_rate,
                    'conversion_rate': conversion_rate
                }
            }
        except Exception as e:
            print(f"❌ Error getting conversion funnel: {e}")
            return {}
    
    def get_lead_distribution(self) -> Dict[str, Any]:
        """Get distribution of leads by status"""
        query = """
            SELECT 
                lead_status,
                COUNT(*) as count,
                ROUND(100.0 * COUNT(*) / SUM(COUNT(*)) OVER (), 2) as percentage
            FROM marketing_leads
            GROUP BY lead_status
            ORDER BY count DESC;
        """
        
        try:
            results = self.db.execute_query(query)
            distribution = {}
            if results:
                for row in results:
                    distribution[row['lead_status']] = {
                        'count': row['count'],
                        'percentage': float(row['percentage'])
                    }
            return distribution
        except Exception as e:
            print(f"❌ Error getting lead distribution: {e}")
            return {}
    
    def get_top_surgeries(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get most inquired about surgeries"""
        query = """
            SELECT 
                UNNEST(surgeries_interested) as surgery,
                COUNT(*) as inquiry_count
            FROM marketing_leads
            WHERE ARRAY_LENGTH(surgeries_interested, 1) > 0
            GROUP BY surgery
            ORDER BY inquiry_count DESC
            LIMIT %s;
        """
        
        try:
            results = self.db.execute_query(query, (limit,))
            return [dict(row) for row in results] if results else []
        except Exception as e:
            print(f"❌ Error getting top surgeries: {e}")
            return []
    
    def get_top_symptoms(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get most reported symptoms"""
        query = """
            SELECT 
                UNNEST(symptoms) as symptom,
                COUNT(*) as mention_count
            FROM marketing_leads
            WHERE ARRAY_LENGTH(symptoms, 1) > 0
            GROUP BY symptom
            ORDER BY mention_count DESC
            LIMIT %s;
        """
        
        try:
            results = self.db.execute_query(query, (limit,))
            return [dict(row) for row in results] if results else []
        except Exception as e:
            print(f"❌ Error getting top symptoms: {e}")
            return []
    
    def get_conversion_events(self, limit: int = 50) -> List[Dict[str, Any]]:
        """Get recent conversion events"""
        query = """
            SELECT * FROM conversion_events
            ORDER BY created_at DESC
            LIMIT %s;
        """
        
        try:
            results = self.db.execute_query(query, (limit,))
            return [dict(row) for row in results] if results else []
        except Exception as e:
            print(f"❌ Error getting conversion events: {e}")
            return []
    
    def get_event_counts(self) -> Dict[str, int]:
        """Get counts of different event types"""
        query = """
            SELECT 
                event_type,
                COUNT(*) as count
            FROM conversion_events
            GROUP BY event_type
            ORDER BY count DESC;
        """
        
        try:
            results = self.db.execute_query(query)
            return {row['event_type']: row['count'] for row in results} if results else {}
        except Exception as e:
            print(f"❌ Error getting event counts: {e}")
            return {}
    
    def get_dashboard_summary(self) -> Dict[str, Any]:
        """
        Get comprehensive dashboard summary
        
        Returns:
            Dict with all key metrics
        """
        return {
            'today': self.get_daily_stats(),
            'week': self.get_weekly_stats(),
            'month': self.get_monthly_stats(),
            'funnel': self.get_conversion_funnel(),
            'lead_distribution': self.get_lead_distribution(),
            'top_surgeries': self.get_top_surgeries(5),
            'top_symptoms': self.get_top_symptoms(5),
            'event_counts': self.get_event_counts()
        }
    
    def get_lead_score_distribution(self) -> Dict[str, Any]:
        """Get distribution of lead scores"""
        query = """
            SELECT 
                CASE 
                    WHEN lead_score >= 80 THEN '80-100 (Hot)'
                    WHEN lead_score >= 50 THEN '50-79 (Warm)'
                    WHEN lead_score >= 20 THEN '20-49 (Cold)'
                    ELSE '0-19 (New)'
                END as score_range,
                COUNT(*) as count
            FROM marketing_leads
            GROUP BY score_range
            ORDER BY score_range DESC;
        """
        
        try:
            results = self.db.execute_query(query)
            return {row['score_range']: row['count'] for row in results} if results else {}
        except Exception as e:
            print(f"❌ Error getting score distribution: {e}")
            return {}
    
    def get_recent_hot_leads(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get most recent hot leads"""
        query = """
            SELECT 
                user_id,
                lead_score,
                last_interaction,
                surgeries_interested,
                booking_intent_detected
            FROM marketing_leads
            WHERE lead_status = 'hot'
            ORDER BY last_interaction DESC
            LIMIT %s;
        """
        
        try:
            results = self.db.execute_query(query, (limit,))
            return [dict(row) for row in results] if results else []
        except Exception as e:
            print(f"❌ Error getting recent hot leads: {e}")
            return []
    
    def get_engagement_metrics(self) -> Dict[str, Any]:
        """Get engagement metrics"""
        try:
            # Average messages per lead
            result = self.db.execute_query("""
                SELECT AVG(total_messages) as avg_messages FROM marketing_leads;
            """)
            avg_messages = float(result[0]['avg_messages']) if result else 0
            
            # Average lead score
            result = self.db.execute_query("""
                SELECT AVG(lead_score) as avg_score FROM marketing_leads;
            """)
            avg_score = float(result[0]['avg_score']) if result else 0
            
            # Leads with multiple interactions
            result = self.db.execute_query("""
                SELECT COUNT(*) as count FROM marketing_leads WHERE total_messages >= 5;
            """)
            highly_engaged = result[0]['count'] if result else 0
            
            return {
                'avg_messages_per_lead': round(avg_messages, 2),
                'avg_lead_score': round(avg_score, 2),
                'highly_engaged_leads': highly_engaged
            }
        except Exception as e:
            print(f"❌ Error getting engagement metrics: {e}")
            return {}
    
    def export_data_for_analysis(self, days: int = 30) -> Dict[str, List]:
        """
        Export data for external analysis
        
        Args:
            days: Number of days to export
        
        Returns:
            Dict with exported data
        """
        try:
            # Daily analytics
            daily_query = """
                SELECT * FROM marketing_analytics
                WHERE date >= CURRENT_DATE - INTERVAL '%s days'
                ORDER BY date DESC;
            """
            daily_data = self.db.execute_query(daily_query, (days,))
            
            # Lead summary
            leads_query = """
                SELECT 
                    user_id,
                    first_contact,
                    total_messages,
                    lead_score,
                    lead_status,
                    booking_intent_detected
                FROM marketing_leads
                WHERE first_contact >= NOW() - INTERVAL '%s days';
            """
            leads_data = self.db.execute_query(leads_query, (days,))
            
            return {
                'daily_analytics': [dict(row) for row in daily_data] if daily_data else [],
                'leads': [dict(row) for row in leads_data] if leads_data else []
            }
        except Exception as e:
            print(f"❌ Error exporting data: {e}")
            return {}
    
    def print_dashboard(self):
        """Print formatted dashboard to console"""
        print("\n" + "="*60)
        print("📊 BRIZ-L MARKETING DASHBOARD")
        print("="*60)
        
        summary = self.get_dashboard_summary()
        
        # Today's stats
        print("\n📅 TODAY:")
        today = summary.get('today', {})
        print(f"  • New Leads: {today.get('total_leads', 0)}")
        print(f"  • Hot Leads: {today.get('hot_leads', 0)}")
        print(f"  • Booking Intents: {today.get('booking_intents', 0)}")
        print(f"  • Follow-ups Sent: {today.get('follow_ups_sent', 0)}")
        
        # Conversion funnel
        print("\n🎯 CONVERSION FUNNEL:")
        funnel = summary.get('funnel', {}).get('funnel', {})
        rates = summary.get('funnel', {}).get('rates', {})
        print(f"  • Total Leads: {funnel.get('total_leads', 0)}")
        print(f"  • Engaged: {funnel.get('engaged_leads', 0)} ({rates.get('engagement_rate', 0)}%)")
        print(f"  • Hot: {funnel.get('hot_leads', 0)} ({rates.get('hot_lead_rate', 0)}%)")
        print(f"  • Booking Intent: {funnel.get('booking_intents', 0)} ({rates.get('intent_rate', 0)}%)")
        print(f"  • Converted: {funnel.get('converted', 0)} ({rates.get('conversion_rate', 0)}%)")
        
        # Top surgeries
        print("\n🏥 TOP SURGERIES:")
        for surgery in summary.get('top_surgeries', [])[:5]:
            print(f"  • {surgery['surgery']}: {surgery['inquiry_count']} inquiries")
        
        # Lead distribution
        print("\n📊 LEAD DISTRIBUTION:")
        for status, data in summary.get('lead_distribution', {}).items():
            print(f"  • {status.upper()}: {data['count']} ({data['percentage']}%)")
        
        print("\n" + "="*60 + "\n")
