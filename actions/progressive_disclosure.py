from typing import Dict, Text, Any, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet

class ActionProgressiveEducation(Action):
    def name(self) -> Text:
        return "action_progressive_education"
    
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        topic = tracker.get_slot("education_topic")
        depth = tracker.get_slot("education_depth")
        
        # Ensure depth is treated as integer
        try:
            depth = int(depth) if depth else 0
        except ValueError:
            depth = 0
        
        # Cataract education example
        if topic == "cataract":
            if depth == 0:
                # Level 1: Simple explanation
                dispatcher.utter_message(text=
                    "Katarakta göz lensinin dumanlı olmasıdır. "
                    "Yaşlanma ilə təbii prosesdir.\n\n"
                    "Daha ətraflı məlumat istəyirsiniz?"
                )
                return [SlotSet("education_depth", 1)]
                
            elif depth == 1:
                # Level 2: Symptoms & impact
                dispatcher.utter_message(text=
                    "Katarakta əlamətləri:\n"
                    "• Dumanlı, bulanıq görmə\n"
                    "• Rəngləri solğun görmə\n"
                    "• İşıqdan rahatsızlıq\n"
                    "• Gecə maşın sürmək çətindir\n\n"
                    "Müalicə haqqında məlumat istəyirsiniz?"
                )
                return [SlotSet("education_depth", 2)]
                
            elif depth == 2:
                # Level 3: Treatment details
                dispatcher.utter_message(text=
                    "Katarakta müalicəsi: Əməliyyat\n\n"
                    "Prosedur:\n"
                    "✅ 15-20 dəqiqə\n"
                    "✅ Ağrısız (lokal anesteziya)\n"
                    "✅ Köhnə lens çıxır, təmiz lens qoyulur\n"
                    "✅ Eyni gün evə\n\n"
                    "Əməliyyat qiymətləri haqqında məlumat istəyirsiniz?"
                )
                return [SlotSet("education_depth", 3)]
                
        # Default behavior if topic unknown or max depth reached
        return []
