"""
Lead Tracking and Scoring System
Tracks every user interaction and calculates lead score
"""

import json
from datetime import datetime
from typing import Dict, List, Any, Optional
from .database import db


class LeadTracker:
    """Tracks and scores leads based on their interactions"""
    
    # Scoring weights
    SCORE_WEIGHTS = {
        'price_inquiry': 30,
        'doctor_inquiry': 20,
        'surgery_inquiry': 15,
        'symptom_mentioned': 25,
        'booking_intent': 40,
        'multiple_messages': 10,
        'return_visit': 15,
        'urgent_symptoms': 35
    }
    
    def __init__(self):
        self.db = db
    
    def create_or_update_lead(self, user_id: str, message: str, 
                             detected_items: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create or update a lead in the database
        
        Args:
            user_id: Unique user identifier
            message: User's message
            detected_items: Dict containing detected symptoms, surgeries, doctors, etc.
        
        Returns:
            Updated lead data with score
        """
        # Check if lead exists
        existing_lead = self.get_lead(user_id)
        
        if existing_lead:
            return self._update_existing_lead(user_id, message, detected_items, existing_lead)
        else:
            return self._create_new_lead(user_id, message, detected_items)
    
    def _create_new_lead(self, user_id: str, message: str, 
                        detected_items: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new lead"""
        
        # Calculate initial score
        initial_score = self._calculate_score(detected_items, is_new=True)
        
        # Determine initial status
        status = self._determine_status(initial_score)
        
        # Prepare conversation history
        conversation = [{
            'timestamp': datetime.now().isoformat(),
            'message': message,
            'items': detected_items
        }]
        
        query = """
            INSERT INTO marketing_leads 
            (user_id, first_contact, last_interaction, total_messages, 
             symptoms, surgeries_interested, doctors_inquired, lead_score, 
             lead_status, booking_intent_detected, conversation_history)
            VALUES (%s, NOW(), NOW(), %s, %s, %s, %s, %s, %s, %s, %s)
            RETURNING *;
        """
        
        params = (
            user_id,
            1,
            detected_items.get('symptoms', []),
            detected_items.get('surgeries', []),
            detected_items.get('doctors', []),
            initial_score,
            status,
            detected_items.get('booking_intent', False),
            json.dumps(conversation)
        )
        
        result = self.db.execute_query(query, params)
        
        # Log conversion events
        self._log_conversion_events(user_id, detected_items)
        
        # Update analytics
        self._update_analytics('new_lead')
        
        print(f"📊 NEW LEAD: {user_id} | Score: {initial_score} | Status: {status}")
        
        return dict(result[0]) if result else {}
    
    def _update_existing_lead(self, user_id: str, message: str, 
                             detected_items: Dict[str, Any], 
                             existing_lead: Dict) -> Dict[str, Any]:
        """Update existing lead"""
        
        # Merge detected items with existing data
        symptoms = list(set(existing_lead.get('symptoms', []) + 
                          detected_items.get('symptoms', [])))
        surgeries = list(set(existing_lead.get('surgeries_interested', []) + 
                           detected_items.get('surgeries', [])))
        doctors = list(set(existing_lead.get('doctors_inquired', []) + 
                         detected_items.get('doctors', [])))
        
        # Update conversation history
        conversation = existing_lead.get('conversation_history', [])
        if isinstance(conversation, str):
            conversation = json.loads(conversation)
        
        conversation.append({
            'timestamp': datetime.now().isoformat(),
            'message': message,
            'items': detected_items
        })
        
        # Calculate new score
        total_messages = existing_lead.get('total_messages', 0) + 1
        detected_items['return_visit'] = True
        detected_items['multiple_messages'] = total_messages >= 5
        
        additional_score = self._calculate_score(detected_items, is_new=False)
        new_score = min(100, existing_lead.get('lead_score', 0) + additional_score)
        
        # Determine new status
        new_status = self._determine_status(new_score)
        
        # Update booking intent
        booking_intent = (existing_lead.get('booking_intent_detected', False) or 
                         detected_items.get('booking_intent', False))
        
        query = """
            UPDATE marketing_leads
            SET last_interaction = NOW(),
                total_messages = %s,
                symptoms = %s,
                surgeries_interested = %s,
                doctors_inquired = %s,
                lead_score = %s,
                lead_status = %s,
                booking_intent_detected = %s,
                conversation_history = %s
            WHERE user_id = %s
            RETURNING *;
        """
        
        params = (
            total_messages,
            symptoms,
            surgeries,
            doctors,
            new_score,
            new_status,
            booking_intent,
            json.dumps(conversation),
            user_id
        )
        
        result = self.db.execute_query(query, params)
        
        # Log conversion events
        self._log_conversion_events(user_id, detected_items)
        
        # Update analytics if status changed
        if new_status != existing_lead.get('lead_status'):
            self._update_analytics('status_change', new_status)
        
        print(f"📊 LEAD UPDATED: {user_id} | Score: {new_score} | Status: {new_status}")
        
        return dict(result[0]) if result else {}
    
    def _calculate_score(self, detected_items: Dict[str, Any], is_new: bool) -> int:
        """Calculate lead score based on detected items"""
        score = 0
        
        for key, weight in self.SCORE_WEIGHTS.items():
            if detected_items.get(key, False):
                score += weight
        
        # Additional scoring logic
        if len(detected_items.get('symptoms', [])) > 0:
            score += self.SCORE_WEIGHTS['symptom_mentioned']
        
        if len(detected_items.get('surgeries', [])) > 1:
            score += 10  # Interested in multiple surgeries
        
        if detected_items.get('urgent_symptoms'):
            score += self.SCORE_WEIGHTS['urgent_symptoms']
        
        return score
    
    def _determine_status(self, score: int) -> str:
        """Determine lead status based on score"""
        if score >= 80:
            return 'hot'
        elif score >= 50:
            return 'warm'
        elif score >= 20:
            return 'cold'
        else:
            return 'new'
    
    def _log_conversion_events(self, user_id: str, detected_items: Dict[str, Any]):
        """Log conversion events for analytics"""
        events_to_log = []
        
        if detected_items.get('price_inquiry'):
            events_to_log.append(('price_inquiry', {'message': 'User asked about price'}))
        
        if detected_items.get('doctor_inquiry'):
            doctors = detected_items.get('doctors', [])
            events_to_log.append(('doctor_inquiry', {'doctors': doctors}))
        
        if detected_items.get('booking_intent'):
            events_to_log.append(('booking_intent', {'detected': True}))
        
        if detected_items.get('urgent_symptoms'):
            events_to_log.append(('urgent_symptoms', {'symptoms': detected_items.get('symptoms', [])}))
        
        for event_type, event_data in events_to_log:
            query = """
                INSERT INTO conversion_events (user_id, event_type, event_data, created_at)
                VALUES (%s, %s, %s, NOW());
            """
            try:
                self.db.execute_query(query, (user_id, event_type, json.dumps(event_data)), fetch=False)
            except Exception as e:
                print(f"⚠️ Error logging event: {e}")
    
    def _update_analytics(self, metric: str, value: str = None):
        """Update daily analytics"""
        try:
            # Ensure today's analytics row exists
            self.db.execute_query("""
                INSERT INTO marketing_analytics (date, total_leads, hot_leads, booking_intents)
                VALUES (CURRENT_DATE, 0, 0, 0)
                ON CONFLICT (date) DO NOTHING;
            """, fetch=False)
            
            # Update specific metric
            if metric == 'new_lead':
                self.db.execute_query("""
                    UPDATE marketing_analytics
                    SET total_leads = total_leads + 1
                    WHERE date = CURRENT_DATE;
                """, fetch=False)
            
            elif metric == 'status_change' and value == 'hot':
                self.db.execute_query("""
                    UPDATE marketing_analytics
                    SET hot_leads = hot_leads + 1
                    WHERE date = CURRENT_DATE;
                """, fetch=False)
        except Exception as e:
            print(f"⚠️ Error updating analytics: {e}")
    
    def get_lead(self, user_id: str) -> Optional[Dict[str, Any]]:
        """Get lead by user_id"""
        query = "SELECT * FROM marketing_leads WHERE user_id = %s;"
        result = self.db.execute_query(query, (user_id,))
        return dict(result[0]) if result else None
    
    def get_hot_leads(self, limit: int = 50) -> List[Dict[str, Any]]:
        """Get all hot leads"""
        query = """
            SELECT * FROM marketing_leads 
            WHERE lead_status = 'hot'
            ORDER BY lead_score DESC, last_interaction DESC
            LIMIT %s;
        """
        results = self.db.execute_query(query, (limit,))
        return [dict(row) for row in results]
    
    def get_leads_for_followup(self) -> List[Dict[str, Any]]:
        """Get leads that need follow-up (not contacted in 24h+)"""
        query = """
            SELECT l.* FROM marketing_leads l
            LEFT JOIN follow_ups f ON l.user_id = f.user_id 
                AND f.follow_up_type = '24h'
            WHERE l.booking_intent_detected = FALSE
                AND l.lead_status IN ('warm', 'hot')
                AND l.last_interaction < NOW() - INTERVAL '24 hours'
                AND f.user_id IS NULL
            ORDER BY l.lead_score DESC;
        """
        results = self.db.execute_query(query)
        return [dict(row) for row in results]
    
    def mark_lead_converted(self, user_id: str):
        """Mark lead as converted (booked appointment)"""
        query = """
            UPDATE marketing_leads
            SET lead_status = 'converted',
                booking_intent_detected = TRUE
            WHERE user_id = %s;
        """
        self.db.execute_query(query, (user_id,), fetch=False)
        
        # Update analytics
        self.db.execute_query("""
            INSERT INTO marketing_analytics (date, booking_intents)
            VALUES (CURRENT_DATE, 1)
            ON CONFLICT (date) 
            DO UPDATE SET booking_intents = marketing_analytics.booking_intents + 1;
        """, fetch=False)
        
        print(f"🎉 CONVERSION: {user_id} marked as converted!")
    
    def get_lead_stats(self) -> Dict[str, Any]:
        """Get overall lead statistics"""
        stats = {}
        
        # Total leads
        result = self.db.execute_query("SELECT COUNT(*) as count FROM marketing_leads;")
        stats['total_leads'] = result[0]['count'] if result else 0
        
        # By status
        result = self.db.execute_query("""
            SELECT lead_status, COUNT(*) as count 
            FROM marketing_leads 
            GROUP BY lead_status;
        """)
        stats['by_status'] = {row['lead_status']: row['count'] for row in result} if result else {}
        
        # Today's leads
        result = self.db.execute_query("""
            SELECT COUNT(*) as count 
            FROM marketing_leads 
            WHERE DATE(first_contact) = CURRENT_DATE;
        """)
        stats['today_leads'] = result[0]['count'] if result else 0
        
        # Hot leads
        result = self.db.execute_query("""
            SELECT COUNT(*) as count 
            FROM marketing_leads 
            WHERE lead_status = 'hot';
        """)
        stats['hot_leads'] = result[0]['count'] if result else 0
        
        return stats
