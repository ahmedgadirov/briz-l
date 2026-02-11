from typing import Dict, Tuple, List, Any
from datetime import datetime, timedelta

class UrgencyCalculator:
    """
    Determines urgency level and recommended timeframe based on severity and risk.
    """
    
    URGENCY_LEVELS = {
        'emergency': {
            'priority': 1,
            'timeframe': 'Dərhal (1-2 saat)',
            'color': '🔴',
            'action': 'immediate_escalation'
        },
        'urgent': {
            'priority': 2,
            'timeframe': '12-24 saat ərzində',
            'color': '🟠',
            'action': 'same_day_booking'
        },
        'soon': {
            'priority': 3,
            'timeframe': '3-7 gün ərzində',
            'color': '🟡',
            'action': 'this_week_booking'
        },
        'routine': {
            'priority': 4,
            'timeframe': '2-4 həftə ərzində',
            'color': '🟢',
            'action': 'flexible_booking'
        },
        'elective': {
            'priority': 5,
            'timeframe': 'Çevikdir',
            'color': '⚪',
            'action': 'informational'
        }
    }
    
    def calculate_urgency(self, 
                          severity_score: float,
                          symptom_details: Dict,
                          risk_factors: List[str]) -> Tuple[str, Dict]:
        """
        Calculate urgency level.
        
        Args:
            severity_score: Adjusted severity (0-10)
            symptom_details: Details from symptom matrix
            risk_factors: Applied risk factors
            
        Returns:
            (urgency_level, urgency_details)
        """
        
        urgency = 'routine' # Default
        
        # Override with symptom matrix urgency if available
        if symptom_details and 'urgency' in symptom_details:
            urgency = symptom_details['urgency']
        else:
            # Calculate from severity score
            if severity_score >= 9:
                urgency = 'emergency'
            elif severity_score >= 7:
                urgency = 'urgent'
            elif severity_score >= 5:
                urgency = 'soon'
            elif severity_score >= 3:
                urgency = 'routine'
            else:
                urgency = 'elective'
        
        # Escalate if high-risk factors present
        # If we have 3+ risk factors, bump up from soon to urgent
        if len(risk_factors) >= 3 and urgency == 'soon':
            urgency = 'urgent'
        # If we have 2+ risk factors, bump up from routine to soon
        elif len(risk_factors) >= 2 and urgency == 'routine':
            urgency = 'soon'
            
        # Ensure we don't downgrade explicit emergencies from symptom matrix
        if symptom_details.get('urgency') == 'emergency':
            urgency = 'emergency'
        
        urgency_details = self.URGENCY_LEVELS.get(urgency, self.URGENCY_LEVELS['routine']).copy()
        urgency_details['severity_score'] = severity_score
        urgency_details['risk_factors_count'] = len(risk_factors)
        
        return urgency, urgency_details
