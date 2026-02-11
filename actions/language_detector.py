from typing import Dict, Text, Any, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet
from langdetect import detect

class ActionDetectLanguage(Action):
    def name(self) -> Text:
        return "action_detect_language"
    
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        user_message = tracker.latest_message.get('text', '')
        
        try:
            detected_lang = detect(user_message)
            
            # Map to supported languages
            if detected_lang in ['az', 'tr']:  # Azerbaijani/Turkish treated as AZ
                language = 'az'
            elif detected_lang == 'ru':
                language = 'ru'
            elif detected_lang == 'en':
                language = 'en'
            else:
                language = 'az'  # Default to AZ
            
            # If switching language, optionally notify (commented out to be less chatty, or logic can be added)
            current_lang = tracker.get_slot("language")
            if current_lang and current_lang != language:
                if language == 'ru':
                    dispatcher.utter_message(text="Переключаюсь на русский язык.")
                elif language == 'en':
                    dispatcher.utter_message(text="Switching to English.")
            
            return [SlotSet("language", language)]
            
        except:
            return [SlotSet("language", "az")]
