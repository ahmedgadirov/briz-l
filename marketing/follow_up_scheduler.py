"""
Follow-up Scheduler - Automates re-engagement with leads
"""

import json
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from .database import db


class FollowUpScheduler:
    """Schedules and manages automated follow-ups with leads"""
    
    FOLLOW_UP_MESSAGES = {
        '24h': [
            "Salam! Mən VERA, dün bizimlə danışmışdınız. 👋\n\nBaşqa sualınız var? Müayinə üçün kömək edə bilərəm? 😊\n\n📞 +994 12 541 19 00",

            "Salam! VERA sizinlə əlaqə saxlayır. 🙂\n\nDünənki söhbətimizə davam edək? Göz sağlamlığınız üçün hər hansı kömək lazımdırsa, buradayıq!\n\n📞 +994 12 541 19 00",

            "Salam! Mən VERA, Briz-L köməkçisiyəm. 👋\n\nDünən bizimlə əlaqə saxlamışdınız. Suallarınıza cavab verə və ya müayinə təyin edə bilərik.\n\n📞 +994 12 541 19 00"
        ],
        '48h': [
            "Salam! Bir neçə gün əvvəl bizimlə danışmışdıq. 👋\n\nGözünüzlə bağlı probleminizlə həll tapdınız? Hələ də kömək lazımdırsa, burdayıq! 🙂\n\n📞 +994 12 541 19 00",
            
            "Salam! İki gün əvvəl məlumat almışdınız. 📝\n\nQərarınızı vermisinizsə və ya sualınız varsa, məmnuniyyətlə cavablandırırıq.\n\n📞 +994 12 541 19 00",
            
            "Salam! Göz sağlamlığınız barədə düşünmüsünüzmü? 🤔\n\nMüayinə üçün vaxt təyin etməyə kömək edə bilərik.\n\n📞 +994 12 541 19 00"
        ],
        '1week': [
            "Salam! Keçən həftə mənimlə yazışmışdınız. 👋\n\nGöz sağlamlığınız vacibdir. İndi müayinəyə yazıla bilərsiniz. Kömək edim? 📞\n\n☎️ +994 12 541 19 00\n📱 WhatsApp: https://wa.me/994555512400",
            
            "Salam! Bir həftə əvvəl bizimlə danışmışdınız. 📅\n\nGöz probleminiz hələ də qalırsa, müayinə vaxtıdır. Sizə kömək edək?\n\n📞 +994 12 541 19 00",
            
            "Salam! Keçən həftə göz sağlamlığı barədə məlumat almışdınız. 👓\n\nErkən müayinə hər zaman yaxşıdır. Vaxt təyin edək?\n\n📞 +994 12 541 19 00"
        ]
    }
    
    def __init__(self):
        self.db = db
    
    def get_leads_needing_followup(self, follow_up_type: str = '24h') -> List[Dict[str, Any]]:
        """
        Get leads that need follow-up based on time elapsed
        
        Args:
            follow_up_type: '24h', '48h', or '1week'
        
        Returns:
            List of leads needing follow-up
        """
        time_intervals = {
            '24h': '24 hours',
            '48h': '48 hours',
            '1week': '7 days'
        }
        
        interval = time_intervals.get(follow_up_type, '24 hours')
        
        query = """
            SELECT l.* FROM marketing_leads l
            LEFT JOIN follow_ups f ON l.user_id = f.user_id 
                AND f.follow_up_type = %s
            WHERE l.booking_intent_detected = FALSE
                AND l.lead_status IN ('warm', 'hot', 'cold')
                AND l.last_interaction < NOW() - INTERVAL %s
                AND f.user_id IS NULL
            ORDER BY l.lead_score DESC
            LIMIT 50;
        """
        
        try:
            results = self.db.execute_query(query, (follow_up_type, interval))
            return [dict(row) for row in results] if results else []
        except Exception as e:
            print(f"❌ Error getting leads for follow-up: {e}")
            return []
    
    def schedule_follow_up(self, user_id: str, follow_up_type: str) -> bool:
        """
        Schedule a follow-up for a lead
        
        Args:
            user_id: User ID to follow up with
            follow_up_type: Type of follow-up ('24h', '48h', '1week')
        
        Returns:
            Boolean indicating success
        """
        query = """
            INSERT INTO follow_ups (user_id, follow_up_type, sent_at, response_received)
            VALUES (%s, %s, NOW(), FALSE);
        """
        
        try:
            self.db.execute_query(query, (user_id, follow_up_type), fetch=False)
            
            # Update analytics
            self.db.execute_query("""
                INSERT INTO marketing_analytics (date, follow_ups_sent)
                VALUES (CURRENT_DATE, 1)
                ON CONFLICT (date) 
                DO UPDATE SET follow_ups_sent = marketing_analytics.follow_ups_sent + 1;
            """, fetch=False)
            
            print(f"📧 Follow-up scheduled: {user_id} ({follow_up_type})")
            return True
        except Exception as e:
            print(f"❌ Error scheduling follow-up: {e}")
            return False
    
    def get_follow_up_message(self, follow_up_type: str, 
                              lead_data: Optional[Dict[str, Any]] = None) -> str:
        """
        Get appropriate follow-up message
        
        Args:
            follow_up_type: Type of follow-up
            lead_data: Optional lead data for personalization
        
        Returns:
            Follow-up message text
        """
        import random
        
        messages = self.FOLLOW_UP_MESSAGES.get(follow_up_type, self.FOLLOW_UP_MESSAGES['24h'])
        base_message = random.choice(messages)
        
        # Personalize based on lead data if available
        if lead_data:
            surgeries = lead_data.get('surgeries_interested', [])
            symptoms = lead_data.get('symptoms', [])
            
            if surgeries:
                surgery = surgeries[0] if surgeries else ''
                base_message += f"\n\n💡 Xatırlatma: {surgery.title()} haqqında danışmışdıq."
            
            if symptoms:
                base_message += "\n\n🩺 Simptomlarınız hələ də davam edirmi?"
        
        return base_message
    
    def mark_response_received(self, user_id: str, follow_up_type: str) -> bool:
        """
        Mark that user responded to follow-up
        
        Args:
            user_id: User ID
            follow_up_type: Type of follow-up
        
        Returns:
            Boolean indicating success
        """
        query = """
            UPDATE follow_ups
            SET response_received = TRUE
            WHERE user_id = %s AND follow_up_type = %s;
        """
        
        try:
            self.db.execute_query(query, (user_id, follow_up_type), fetch=False)
            
            # Update analytics
            self.db.execute_query("""
                INSERT INTO marketing_analytics (date, follow_up_responses)
                VALUES (CURRENT_DATE, 1)
                ON CONFLICT (date) 
                DO UPDATE SET follow_up_responses = marketing_analytics.follow_up_responses + 1;
            """, fetch=False)
            
            print(f"✅ Follow-up response recorded: {user_id}")
            return True
        except Exception as e:
            print(f"❌ Error marking response: {e}")
            return False
    
    def process_all_followups(self) -> Dict[str, int]:
        """
        Process all pending follow-ups (run this periodically)
        
        Returns:
            Dict with counts of follow-ups processed
        """
        results = {
            '24h_sent': 0,
            '48h_sent': 0,
            '1week_sent': 0,
            'total_sent': 0
        }
        
        # Process each follow-up type
        for follow_up_type in ['24h', '48h', '1week']:
            leads = self.get_leads_needing_followup(follow_up_type)
            
            for lead in leads:
                success = self.schedule_follow_up(lead['user_id'], follow_up_type)
                if success:
                    results[f'{follow_up_type}_sent'] += 1
                    results['total_sent'] += 1
                    
                    # Note: Actual message sending would be handled by
                    # Telegram bot or messaging service integration
                    message = self.get_follow_up_message(follow_up_type, lead)
                    print(f"📨 Follow-up message for {lead['user_id']}:\n{message}\n")
        
        print(f"📊 Follow-up batch complete: {results['total_sent']} messages processed")
        return results
    
    def get_follow_up_effectiveness(self) -> Dict[str, Any]:
        """
        Get statistics on follow-up effectiveness
        
        Returns:
            Dict with follow-up stats
        """
        try:
            # Total follow-ups sent
            result = self.db.execute_query("""
                SELECT COUNT(*) as total FROM follow_ups;
            """)
            total_sent = result[0]['total'] if result else 0
            
            # Follow-ups with responses
            result = self.db.execute_query("""
                SELECT COUNT(*) as total FROM follow_ups WHERE response_received = TRUE;
            """)
            total_responses = result[0]['total'] if result else 0
            
            # Response rate by type
            result = self.db.execute_query("""
                SELECT 
                    follow_up_type,
                    COUNT(*) as sent,
                    SUM(CASE WHEN response_received THEN 1 ELSE 0 END) as responses,
                    ROUND(100.0 * SUM(CASE WHEN response_received THEN 1 ELSE 0 END) / COUNT(*), 2) as response_rate
                FROM follow_ups
                GROUP BY follow_up_type;
            """)
            
            by_type = {}
            if result:
                for row in result:
                    by_type[row['follow_up_type']] = {
                        'sent': row['sent'],
                        'responses': row['responses'],
                        'response_rate': float(row['response_rate']) if row['response_rate'] else 0
                    }
            
            return {
                'total_sent': total_sent,
                'total_responses': total_responses,
                'overall_response_rate': round(100 * total_responses / total_sent, 2) if total_sent > 0 else 0,
                'by_type': by_type
            }
        except Exception as e:
            print(f"❌ Error getting follow-up stats: {e}")
            return {}
    
    def get_recent_followups(self, limit: int = 20) -> List[Dict[str, Any]]:
        """
        Get recent follow-ups
        
        Args:
            limit: Number of recent follow-ups to retrieve
        
        Returns:
            List of recent follow-ups
        """
        query = """
            SELECT f.*, l.lead_score, l.lead_status
            FROM follow_ups f
            JOIN marketing_leads l ON f.user_id = l.user_id
            ORDER BY f.sent_at DESC
            LIMIT %s;
        """
        
        try:
            results = self.db.execute_query(query, (limit,))
            return [dict(row) for row in results] if results else []
        except Exception as e:
            print(f"❌ Error getting recent follow-ups: {e}")
            return []
    
    def should_send_followup(self, user_id: str) -> Dict[str, Any]:
        """
        Determine if and what type of follow-up should be sent
        
        Args:
            user_id: User ID to check
        
        Returns:
            Dict with recommendation
        """
        # Get lead data
        query = "SELECT * FROM marketing_leads WHERE user_id = %s;"
        result = self.db.execute_query(query, (user_id,))
        
        if not result:
            return {'should_send': False, 'reason': 'Lead not found'}
        
        lead = dict(result[0])
        
        # Don't send if already converted
        if lead['booking_intent_detected'] or lead['lead_status'] == 'converted':
            return {'should_send': False, 'reason': 'Already converted'}
        
        # Calculate time since last interaction
        last_interaction = lead['last_interaction']
        now = datetime.now()
        time_diff = now - last_interaction
        
        # Determine follow-up type
        if time_diff >= timedelta(days=7):
            follow_up_type = '1week'
        elif time_diff >= timedelta(hours=48):
            follow_up_type = '48h'
        elif time_diff >= timedelta(hours=24):
            follow_up_type = '24h'
        else:
            return {'should_send': False, 'reason': 'Too soon'}
        
        # Check if this type of follow-up was already sent
        check_query = """
            SELECT * FROM follow_ups 
            WHERE user_id = %s AND follow_up_type = %s;
        """
        existing = self.db.execute_query(check_query, (user_id, follow_up_type))
        
        if existing:
            return {'should_send': False, 'reason': f'{follow_up_type} already sent'}
        
        return {
            'should_send': True,
            'follow_up_type': follow_up_type,
            'lead_score': lead['lead_score'],
            'time_since_last': str(time_diff)
        }
