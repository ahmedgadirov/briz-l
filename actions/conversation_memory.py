from typing import Dict, Text, Any, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet

class ActionRecapConversation(Action):
    def name(self) -> Text:
        return "action_recap_conversation"
    
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        # Collect important info from conversation
        # Note: some slots like patient_name might need to be added to domain if not present
        patient_name = tracker.get_slot("patient_name") # Assumes slot exists or will be added
        concern = tracker.get_slot("patient_concern")
        symptoms = tracker.get_slot("symptoms") # Assumes slot exists
        
        # If symptoms slot is empty, try to construct from other slots
        if not symptoms and concern:
             symptoms = concern
             
        duration = tracker.get_slot("symptom_duration")
        urgency = tracker.get_slot("urgency_level")
        
        recap = "📋 Söhbətimizin xülasəsi:\n\n"
        
        if patient_name:
            recap += f"👤 Ad: {patient_name}\n"
        if concern:
            recap += f"🎯 Problem: {concern}\n"
        if symptoms and symptoms != concern:
            recap += f"⚕️ Əlamətlər: {symptoms}\n"
        if duration:
            recap += f"⏰ Müddət: {duration}\n"
        if urgency:
            recap += f"🚨 Təcililik: {urgency}\n"
        
        recap += "\nDüzgündür? Düzəliş etmək istəyirsiniz?"
        
        dispatcher.utter_message(text=recap)
        
        return []
