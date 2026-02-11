from typing import Dict, Text, Any, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet

class ActionWarmHandoff(Action):
    def name(self) -> Text:
        return "action_warm_handoff"
    
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        profile = tracker.get_slot("patient_profile")
        patient_name = tracker.get_slot("patient_name") or "Hörmətli pasiyent"
        urgency = tracker.get_slot("urgency_level")
        
        # Personalized handoff message
        if urgency == "emergency":
            message = f"""{patient_name}, vəziyyətiniz təcilidir.

Koordinatorumuz Əli Məmmədov SİZİ GÖZLƏYİR:
📱 WhatsApp: https://wa.me/994555512400
☎️ Tel: +994 12 541 19 00

Ona deyə bilərsiniz:
"{tracker.get_slot('patient_concern')}"

O sizin bütün məlumatlarınıza baxıb və DƏRHAL kömək edəcək.

❗ 15 dəqiqə ərzində əlaqə saxlayın!"""

        else:
            concern = tracker.get_slot('patient_concern') or "ümumi müayinə"
            duration = tracker.get_slot('symptom_duration') or "qeyd olunmayıb"
            preferred_date = tracker.get_slot('preferred_time') or "dəqiqləşdirilməyib" # corrected slot name
            
            message = f"""{patient_name}, məlumatlarınızı koordinatorumuza ötürdüm.

Koordinatorumuz Əli Məmmədov sizinlə əlaqə saxlayacaq:
📱 WhatsApp: https://wa.me/994555512400
☎️ Tel: +994 12 541 19 00

O bilir ki:
✅ Sizin problemiz: {concern}
✅ Müddət: {duration}
✅ Üstünlük: {preferred_date}

30 dəqiqə ərzində cavab alacaqsınız.

Başqa sualınız var?"""
        
        dispatcher.utter_message(text=message)
        
        # In production: trigger CRM notification, SMS to coordinator
        
        return [SlotSet("handoff_completed", True)]
