import yaml
from typing import Dict, Text, Any, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet

class ActionProvideReassurance(Action):
    def name(self) -> Text:
        return "action_provide_reassurance"
    
    def __init__(self):
        # Load medical education content
        try:
            with open('data/medical_education.yml', 'r', encoding='utf-8') as f:
                self.education_data = yaml.safe_load(f)
        except Exception as e:
            print(f"Error loading medical education data: {e}")
            self.education_data = {}
    
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        condition = tracker.get_slot("patient_concern")
        emotion = tracker.get_slot("patient_emotion")
        
        # If patient shows fear, provide reassurance
        if emotion == "fear" and condition:
            condition_key = self._map_to_condition_key(condition)
            
            if condition_key and condition_key in self.education_data.get('eye_conditions', {}):
                data = self.education_data['eye_conditions'][condition_key]
                
                message = f"""💙 {data['reassurance']}

📚 {data['simple_explanation']}

{data['what_to_expect']}

📊 Uğur nisbəti: {data['success_rate']}

Başqa sualınız var?"""
                
                dispatcher.utter_message(text=message)
            else:
                 # Default reassurance if specific condition not found
                 dispatcher.utter_message(text="Narahat olmayın, həkimlərimiz çox təcrübəlidir. Sizi müayinə edib ən yaxşı məsləhəti verəcəklər.")
        
        return []
    
    def _map_to_condition_key(self, concern: str) -> str:
        if not concern:
            return None
            
        concern_lower = concern.lower()
        mapping = {
            "katarakta": "cataract",
            "mirvari": "cataract",
            "lazer": "lasik",
            "excimer": "lasik",
            "gözlük": "lasik",
            "minus": "lasik",
            "plus": "lasik",
            "astigmat": "lasik"
        }
        
        for key, value in mapping.items():
            if key in concern_lower:
                return value
        
        return None
