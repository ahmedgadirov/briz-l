from typing import Dict, Text, Any, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet

class ActionSmartFollowUp(Action):
    """Ask contextually relevant follow-up questions"""
    
    def name(self) -> Text:
        return "action_smart_follow_up"
    
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        concern = tracker.get_slot("patient_concern")
        age = tracker.get_slot("patient_age") # Assumes patient_age slot exists
        
        # Context-specific questions
        if concern:
            concern_lower = str(concern).lower()
            if "katarakta" in concern_lower or "mirvari" in concern_lower:
                if age and int(age) < 50:
                    # Unusual for young patient
                    dispatcher.utter_message(text=
                        "Katarakta adətən 60+ yaşda olur. "
                        "Sizdə travma, şəkərli diabet, və ya gözə zərbə olubmu?"
                    )
                else:
                    dispatcher.utter_message(text=
                        "Katarakta diaqnozu qoyulubmu, "
                        "yoxsa dumanlı görmə probleminiz var?"
                    )
            
            elif "lazer" in concern_lower or "gözlük" in concern_lower or "eynek" in concern_lower:
                dispatcher.utter_message(text=
                    "Lazer əməliyyatı üçün:\n"
                    "• Yaxıngörmə (minus)?\n"
                    "• Uzaqgörmə (plus)?\n"
                    "• Astiqmatizm?\n\n"
                    "Hansı probleminiz var?"
                )
        
        return []
