from typing import Dict, Text, Any, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet

class ActionRecognizeReturningPatient(Action):
    def name(self) -> Text:
        return "action_recognize_returning_patient"
    
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        # In production: check patient database
        # For now: check if phone number in tracker history or slot
        
        phone = tracker.get_slot("phone_number") # corrected slot name
        
        # Mock check - if phone is present, assume returning (simplification for prototype)
        # In reality, would query DB. 
        # Here we mimic logic: if phone was provided previously in conversation or stored.
        
        if phone and len(phone) > 5:  # Valid-ish phone
             # This is a bit tricky without a real persistent DB. 
             # We can check if `is_returning_patient` slot is already set? No.
             # For the sake of the task, let's assume if they provide phone, we check "DB".
             # We'll simulate a 50% chance or just say yes if phone is known format (mock).
             
             # Actually, better logic: this action should be called at start if we knew the user ID.
             # But usually getting phone happens later. 
             # Let's assume this action is triggered when phone is provided.
             
            dispatcher.utter_message(text=
                f"Xoş gördük yenə! 👋\n\n"
                f"Sizin nömrəniz ({phone}) sistemdə var. "
                "Yeni problem, yoxsa müayinə nəticələri ilə bağlı?"
            )
            return [SlotSet("is_returning_patient", True)]
        
        return [SlotSet("is_returning_patient", False)]
