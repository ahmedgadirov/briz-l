from typing import Dict, Text, Any, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet
import json

class ActionBuildPatientProfile(Action):
    def name(self) -> Text:
        return "action_build_patient_profile"
    
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        # Build comprehensive profile
        profile = {
            "name": tracker.get_slot("patient_name"), # Assumes slot exists
            "age": tracker.get_slot("patient_age"),
            "phone": tracker.get_slot("phone_number"), # corrected slot name from plan
            "concern": tracker.get_slot("patient_concern"),
            "symptoms": tracker.get_slot("symptoms"), # Assumes slot exists
            "duration": tracker.get_slot("symptom_duration"),
            "severity": tracker.get_slot("symptom_severity"),
            "urgency": tracker.get_slot("urgency_level"),
            "emotion": tracker.get_slot("patient_emotion"),
            "preferred_date": tracker.get_slot("preferred_time"), # corrected slot name from plan
            "language": tracker.get_slot("language"),
            "conversation_summary": self._generate_summary(tracker)
        }
        
        # Store for coordinator handoff
        # In production: save to CRM/database
        
        return [SlotSet("patient_profile", json.dumps(profile, ensure_ascii=False))]
    
    def _generate_summary(self, tracker: Tracker) -> str:
        events = tracker.events
        user_messages = [e for e in events if e.get("event") == "user"]
        
        summary = f"Conversation length: {len(user_messages)} messages"
        emotion = tracker.get_slot('patient_emotion')
        if emotion:
             summary += f" | Emotional state: {emotion}"
        
        return summary
