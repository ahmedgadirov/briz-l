from typing import Dict, Text, Any, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet

class ActionDetectEmotion(Action):
    def name(self) -> Text:
        return "action_detect_emotion"
    
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        user_message = tracker.latest_message.get('text', '').lower()
        
        # Pain indicators
        pain_words = ['ağrıyır', 'ağrı', 'sancı', 'yanır', 'batır', 'dözülməz']
        
        # Fear/worry indicators
        fear_words = ['qorxuram', 'narahatam', 'təşvişdəyəm', 'çox pisdir', 'ölürəm']
        
        # Urgency indicators
        urgent_words = ['təcili', 'dərhal', 'tez', 'indi', 'gözləyə bilmirəm']
        
        # Frustration indicators
        frustration_words = ['başa düşmürəm', 'yenə', 'neçə dəfə', 'heç kəs', 'yoruldum']
        
        emotion = "neutral"
        urgency = "routine"
        
        if any(word in user_message for word in pain_words):
            emotion = "pain"
        if any(word in user_message for word in fear_words):
            emotion = "fear"
        if any(word in user_message for word in urgent_words):
            urgency = "urgent"
        if any(word in user_message for word in frustration_words):
            emotion = "frustration"
        
        return [
            SlotSet("patient_emotion", emotion),
            SlotSet("urgency_level", urgency)
        ]
