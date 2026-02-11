from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet
import sys
import os
import json

# Add project root to path so we can import triage_system
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from triage_system.core.triage_decision import TriageDecisionEngine
except ImportError:
    # Fallback for when running in some environments where path might be different
    sys.path.append('.')
    from triage_system.core.triage_decision import TriageDecisionEngine

class ActionTriagePatient(Action):
    
    def __init__(self):
        super().__init__()
        self.triage_engine = TriageDecisionEngine()
    
    def name(self) -> Text:
        return "action_triage_patient"
    
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        # Gather patient data
        patient_data = {
            'id': tracker.sender_id,
            'age': tracker.get_slot('patient_age'),
            'has_diabetes': tracker.get_slot('has_diabetes'),
            'previous_retinal_detachment': tracker.get_slot('previous_retinal_detachment'),
            'only_functional_eye': tracker.get_slot('only_functional_eye'),
            'bilateral_symptoms': tracker.get_slot('bilateral_symptoms'),
            'is_pregnant': tracker.get_slot('is_pregnant'),
            'immunocompromised': tracker.get_slot('immunocompromised'),
            'symptom_duration': tracker.get_slot('symptom_duration')
        }
        
        # Get user message - use the latest user message text
        user_message = tracker.latest_message.get('text', '')
        
        # Also check slots for specific symptom info if available
        symptom_concern = tracker.get_slot('patient_concern')
        if symptom_concern:
             user_message += f" {symptom_concern}"
             
        language = tracker.get_slot('language') or 'az'
        
        # Run triage
        try:
            triage_report = self.triage_engine.triage(
                user_message,
                patient_data,
                language
            )
            
            # Log triage for audit (in a real app this would go to a secure log)
            print(f"[TRIAGE REPORT] {json.dumps(triage_report, indent=2, ensure_ascii=False)}")
            
            # Format response based on urgency
            response = self._format_triage_response(triage_report, language)
            dispatcher.utter_message(text=response)
            
            # Return slot updates
            return [
                SlotSet("symptom_severity", str(triage_report['adjusted_severity'])),
                SlotSet("urgency_level", triage_report['urgency_level']),
                SlotSet("triage_protocol", triage_report['protocol']),
                # SlotSet("requires_immediate_escalation", triage_report['urgency_level'] == 'emergency'),
                SlotSet("triage_report", json.dumps(triage_report))
            ]
            
        except Exception as e:
            print(f"Error in triage action: {e}")
            dispatcher.utter_message(text="Sistemsəl xəta baş verdi, lütfən birbaşa əlaqə saxlayın.")
            return []
    
    def _format_triage_response(self, report: Dict, language: str) -> str:
        """Format triage response for patient."""
        
        # urgency = report['urgency_level']
        details = report['urgency_details']
        
        response = f"{details['color']} **TRİAJ QİYMƏTLƏNDİRMƏ**\n\n"
        
        # Severity indicator
        severity_val = int(report['adjusted_severity'])
        severity_bar = "▓" * severity_val + "░" * (10 - severity_val)
        response += f"Ciddiyyət: [{severity_bar}] {report['adjusted_severity']}/10\n\n"
        
        # Risk factors
        if report['risk_factors']:
            response += "⚠️ **Risk faktorları:**\n"
            for factor in report['risk_factors']:
                response += f"  • {factor}\n"
            response += "\n"
        
        # Safety alerts
        if report.get('safety_alerts'):
            response += "🚨 **DİQQƏT:**\n"
            for alert in report['safety_alerts']:
                response += f"  {alert}\n"
            response += "\n"
        
        # Timeframe
        # Helper to get recommendations based on index
        # This is a simplified view, the real reponse is in recommendations list
        
        # Recommendations
        response += "📋 **TÖVSİYƏLƏR:**\n"
        for i, rec in enumerate(report['recommendations'], 1):
            response += f"{i}. {rec}\n"
            
        return response
