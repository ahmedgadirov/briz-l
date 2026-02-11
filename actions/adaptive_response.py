from typing import Dict, Text, Any, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet

class ActionAdaptiveResponse(Action):
    def name(self) -> Text:
        return "action_adaptive_response"
    
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        emotion = tracker.get_slot("patient_emotion")
        urgency = tracker.get_slot("urgency_level")
        
        # Adapt response based on emotion
        if emotion == "pain":
            dispatcher.utter_message(response="utter_acknowledge_pain")
        elif emotion == "fear":
            dispatcher.utter_message(response="utter_acknowledge_fear")
        elif emotion == "frustration":
            dispatcher.utter_message(response="utter_acknowledge_frustration")
        elif emotion == "worry": # Added worry check even if not explicitly in detect logic yet, good practice
             dispatcher.utter_message(response="utter_acknowledge_worry")

        
        # Adapt next action based on urgency
        if urgency in ["urgent", "emergency"]:
            dispatcher.utter_message(
                text="Bu təcili vəziyyətdir. Dərhal əlaqə saxlayın:\n"
                     "📱 WhatsApp: https://wa.me/994555512400\n"
                     "☎️ Telefon: +994 12 541 19 00"
            )
        
        return []
